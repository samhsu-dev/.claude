#!/usr/bin/env python3
"""Read-only metadata audit of a local Zotero library. Copies zotero.sqlite with its write-ahead log (never opens
the live file), runs local checks, optionally verifies papers against Crossref, and prints one JSON report.

Usage: zotero_audit.py [--crossref] [--library NAME_OR_ID] [--limit N] [--db PATH]
Env:   ZOTERO_AUDIT_MAILTO  contact address sent to Crossref's polite pool (optional).
"""
import argparse, json, os, re, shutil, sqlite3, tempfile, time, unicodedata, urllib.error, urllib.parse, urllib.request
from collections import defaultdict
from datetime import date

PAPER_TYPES = ("journalArticle", "conferencePaper", "preprint", "bookSection", "report", "thesis", "book")
MARKER = re.compile(r"approximate|forthcoming|placeholder|to be confirmed|\bTBD\b", re.I)
PREFIX = re.compile(r"^\s*(\d{1,3}[\).:]|\[\d{1,3}\]|\(\d{1,3}\))\s+")
CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯]")
BAD_KEY = re.compile(r"^_|https|^$")
ARXIV = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:\s*|10\.48550/arxiv\.)(\d{4}\.\d{4,5})", re.I)
ARXIV_DOI = re.compile(r"10\.48550/arxiv\.", re.I)


def fold(s):
    return unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", "", s or "")).encode("ascii", "ignore").decode().lower()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", fold(s))


def words(s):
    return set(re.findall(r"[a-z0-9]{3,}", fold(s)))


def same_work_signal(local, cr):
    """Titles share the part before the colon, or at least 30% of their words."""
    a, b = words(local), words(cr["title"] + " " + cr["subtitle"])
    head = lambda t: norm(t.split(":")[0]) if ":" in t else None
    return bool(head(local) and head(local) == head(cr["title"])) or (bool(a and b) and len(a & b) / len(a | b) >= 0.3)


def author_overlap(local, cr):
    fams = [norm(x) for x in cr if x]
    return sum(1 for a in local if norm(a) and any(f and (f in norm(a) or norm(a) in f) for f in fams))


def snapshot(db):
    """Copy the database with its write-ahead log; opening the copy replays the log, so writes Zotero has not
    checkpointed yet are visible. The log is copied first and the copy is retried while either file changes."""
    out = os.path.join(tempfile.mkdtemp(prefix="zotero-audit-"), "zotero.sqlite")
    pair = [(p, out + p[len(db):]) for p in (db + "-wal", db) if os.path.exists(p)]
    for _ in range(3):
        before = [os.stat(p).st_mtime_ns for p, _ in pair]
        for p, q in pair:
            shutil.copyfile(p, q)
        if before == [os.stat(p).st_mtime_ns for p, _ in pair]:
            break
    return sqlite3.connect(out), os.path.dirname(out)


def libraries(c):
    names = {1: "My Library"}
    for lib_id, name in c.execute("select libraryID, name from groups"):
        names[lib_id] = name
    return names


def load_items(c, lib_filter):
    rows = c.execute(f"""select i.itemID, i.key, i.libraryID, t.typeName from items i join itemTypes t using(itemTypeID)
        where i.itemID not in (select itemID from deletedItems)
          and t.typeName not in ('attachment', 'note', 'annotation')""").fetchall()
    items = []
    for iid, key, lib, tn in rows:
        if lib_filter is not None and lib != lib_filter:
            continue
        f = dict(c.execute("""select f.fieldName, v.value from itemData d join fields f using(fieldID)
            join itemDataValues v using(valueID) where d.itemID=?""", (iid,)))
        authors = [r[0] for r in c.execute("""select cr.lastName from itemCreators ic join creators cr using(creatorID)
            where ic.itemID=? order by orderIndex""", (iid,))]
        doi = f.get("DOI")
        if not doi and "DOI:" in (f.get("extra") or ""):
            doi = re.search(r"DOI:\s*(\S+)", f["extra"]).group(1)
        items.append({"key": key, "library": lib, "type": tn, "f": f, "authors": authors, "doi": (doi or "").lower() or None})
    return items


def local_checks(it, this_year):
    f, out = it["f"], []
    title = f.get("title") or ""
    if MARKER.search(f.get("extra") or ""):
        out.append({"check": "unverified_marker", "detail": (f.get("extra") or "").split("\n")[0][:160]})
    if it["type"] in PAPER_TYPES and not it["doi"] and not re.search(r"arxiv", f.get("url") or "", re.I):
        out.append({"check": "paper_without_doi"})
    if PREFIX.search(title):
        out.append({"check": "title_list_prefix", "detail": PREFIX.search(title).group(0).strip()})
    if "  " in title or title != title.strip():
        out.append({"check": "title_whitespace"})
    if not title.strip():
        out.append({"check": "title_empty"})
    st = f.get("shortTitle") or ""
    if st and CJK.search(st) and not CJK.search(title):
        out.append({"check": "short_title_language_mismatch", "detail": st[:80]})
    if "citationKey" in f and BAD_KEY.search(f["citationKey"]):
        out.append({"check": "citation_key_malformed", "detail": f["citationKey"]})
    m = re.search(r"\b(1[89]\d\d|20\d\d)\b", f.get("date") or "")
    if f.get("date") and not m:
        out.append({"check": "date_unparseable", "detail": f["date"]})
    elif m and it["type"] in PAPER_TYPES and not (1950 <= int(m.group(1)) <= this_year + 1):
        out.append({"check": "date_out_of_range", "detail": f["date"]})
    return out


def duplicate_groups(items):
    groups = []
    for label, keyf in [("doi", lambda i: i["doi"]), ("title", lambda i: norm(i["f"].get("title")) if len(norm(i["f"].get("title"))) > 15 else None),
                        ("url", lambda i: (i["f"].get("url") or "").rstrip("/").lower() or None)]:
        by = defaultdict(list)
        for it in items:
            k = keyf(it)
            if k:
                by[(it["library"], k)].append(it)
        for (lib, k), its in by.items():
            if len(its) > 1:
                groups.append({"by": label, "library": lib, "value": k[:120],
                               "items": [{"key": i["key"], "type": i["type"], "date": i["f"].get("date")} for i in its]})
    return groups


class Api:
    """JSON GET with retry and backoff; 400/404 return None. interval spaces requests to a rate-limited service."""

    def __init__(self, base, headers, interval=0.0, attempts=5, max_errors=None):
        self.base, self.headers, self.interval, self.last, self.errors = base, headers, interval, 0.0, 0
        self.attempts, self.max_errors, self.streak, self.disabled = attempts, max_errors, 0, False

    def get(self, path):
        """Optional sources pass max_errors: after that many consecutive failed lookups the source is disabled
        for the run and later lookups return None at once, so a rate-limited source cannot stall the audit."""
        if self.disabled:
            return None
        r = self._get(path)
        self.streak = self.streak + 1 if r is False else 0
        if self.max_errors and self.streak >= self.max_errors:
            self.disabled = True
        return None if r is False else r

    def _get(self, path):
        req = urllib.request.Request(self.base + path, headers=self.headers)
        for attempt in range(self.attempts):
            time.sleep(max(0.0, self.last + self.interval - time.time()))
            self.last = time.time()
            try:
                return json.load(urllib.request.urlopen(req, timeout=30))
            except urllib.error.HTTPError as e:
                if e.code in (400, 404):
                    return None
                time.sleep(2 ** attempt * (5 if e.code == 429 else 1))
            except Exception:
                time.sleep(2 ** attempt)
        self.errors += 1
        return False


class Sources:
    """Crossref holds the authoritative record per DOI; Semantic Scholar links arXiv IDs and titles to DOIs."""

    def __init__(self):
        mail = os.environ.get("ZOTERO_AUDIT_MAILTO")
        ua = {"User-Agent": "zotero-audit" + (f" (mailto:{mail})" if mail else "")}
        key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        self.cr = Api("https://api.crossref.org", ua)
        self.s2 = Api("https://api.semanticscholar.org/graph/v1", {**ua, **({"x-api-key": key} if key else {})},
                      1.0 if key else 3.0, attempts=3, max_errors=5)
        self.works = {}

    @property
    def errors(self):
        return self.cr.errors + self.s2.errors

    def work(self, doi):
        if doi not in self.works:
            w = self.cr.get("/works/" + urllib.parse.quote(doi))
            self.works[doi] = cr_summary(w["message"]) if w else None
        return self.works[doi]

    def search(self, title, author):
        q = urllib.parse.urlencode({"query.bibliographic": title[:200], "query.author": author, "rows": 5})
        return [cr_summary(w) for w in ((self.cr.get("/works?" + q) or {}).get("message") or {}).get("items", [])]

    def s2_doi(self, path):
        """Published DOI Semantic Scholar records for a paper; arXiv DOIs do not count as published."""
        r = self.s2.get(path + ("&" if "?" in path else "?") + "fields=externalIds") or {}
        r = (r.get("data") or [r])[0]
        doi = (r.get("externalIds") or {}).get("DOI")
        return doi.lower() if doi and not ARXIV_DOI.match(doi) else None

    def doi_registered(self, doi):
        """Ask the DOI handle service; covers DataCite DOIs (arXiv, LIPIcs) that Crossref does not index."""
        try:
            r = json.load(urllib.request.urlopen("https://doi.org/api/handles/" + urllib.parse.quote(doi), timeout=30))
            return r.get("responseCode") == 1
        except Exception:
            return False


def cr_summary(w):
    dp = (w.get("issued") or {}).get("date-parts", [[None]])[0]
    return {"doi": w.get("DOI"), "title": re.sub(r"<[^>]+>|\s+", " ", (w.get("title") or [""])[0]).strip(), "subtitle": (w.get("subtitle") or [""])[0],
            "container": (w.get("container-title") or [None])[0], "date": "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(dp)) if dp and dp[0] else None,
            "pages": w.get("page"), "volume": w.get("volume"), "issue": w.get("issue"),
            "authors": [a.get("family") for a in w.get("author", [])]}


def title_matches(local, cr):
    """True when the local title equals the Crossref title, title+subtitle, or extends a Crossref title that lacks its subtitle."""
    lt, t, full = norm(local), norm(cr["title"]), norm(cr["title"] + cr["subtitle"])
    return bool(lt) and (lt in (t, full) or (len(t) > 10 and lt.startswith(t)))


def match(it, s):
    """Evidence that record s describes item it: title relation, author overlap, full author-list equality, year gap."""
    title = it["f"].get("title") or ""
    m = re.search(r"\d{4}", it["f"].get("date") or "")
    have = bool(it["authors"] and s["authors"])
    return {"title": "exact" if title_matches(title, s) else "similar" if same_work_signal(title, s) else "different",
            "authors": author_overlap(it["authors"], s["authors"]) >= min(2, len(it["authors"])) if have else None,
            "all_authors": have and len(it["authors"]) == len(s["authors"]) and author_overlap(it["authors"], s["authors"]) == len(s["authors"]),
            "year_gap": abs(int(m.group(0)) - int(s["date"][:4])) if m and s["date"] else None}


def discover(it, src):
    """Find the published DOI for an item that lacks one. Each candidate collects evidence paths:
    arxiv_link (Semantic Scholar maps the arXiv ID to the DOI), crossref_search, s2_title_match.
    Confirmed: authors overlap and (arxiv_link, or year gap <= 1 with two agreeing paths, an exact title,
    or an identical author list). A larger year gap marks another version or edition, never the same record."""
    f, cands = it["f"], defaultdict(set)
    ax = ARXIV.search(" ".join(filter(None, (f.get("url"), f.get("extra"), it["doi"]))))
    if ax and (d := src.s2_doi(f"/paper/arXiv:{ax.group(1)}")):
        cands[d].add("arxiv_link")
    if f.get("title") and it["authors"]:
        for s in src.search(f["title"], it["authors"][0]):
            if s["doi"] and s["authors"] and author_overlap(it["authors"][:1], s["authors"][:1]):
                src.works.setdefault(s["doi"].lower(), s)
                cands[s["doi"].lower()].add("crossref_search")
        if d := src.s2_doi("/paper/search/match?" + urllib.parse.urlencode({"query": f["title"][:200]})):
            cands[d].add("s2_title_match")
    best = None
    for doi, paths in cands.items():
        s = src.work(doi)
        if not s:
            continue
        m = match(it, s)
        if m["authors"] is False or (m["title"] == "different" and "arxiv_link" not in paths):
            continue
        near_year = m["year_gap"] is None or m["year_gap"] <= 1  # a larger gap means another version or edition
        ok = bool(m["authors"]) and ("arxiv_link" in paths or near_year and (len(paths) >= 2 or m["title"] == "exact" or m["all_authors"]))
        rank = (ok, len(paths), m["title"] == "exact")
        if not best or rank > best[0]:
            best = (rank, {"check": "doi_found" if ok else "possible_wrong_title", "crossref": s, "evidence": sorted(paths), "match": m})
    return [best[1]] if best else []


def crossref_checks(it, src):
    f, out = it["f"], []
    if it["type"] not in PAPER_TYPES:
        return out
    if it["doi"] and ARXIV_DOI.match(it["doi"]):
        return discover(it, src)
    if it["doi"]:
        s = src.work(it["doi"])
        if not s:
            return [] if src.doi_registered(it["doi"]) else [{"check": "doi_not_found", "detail": it["doi"]}]
        if not title_matches(f.get("title"), s):
            out.append({"check": "title_differs_from_doi_record", "crossref": s})
        if it["authors"] and s["authors"] and not author_overlap(it["authors"][:1], s["authors"][:1]):
            out.append({"check": "first_author_differs", "detail": [it["authors"][0], s["authors"][0]]})
        m = re.search(r"\d{4}", f.get("date") or "")
        if m and s["date"] and m.group(0) != s["date"][:4]:
            out.append({"check": "year_differs", "detail": [f.get("date"), s["date"]]})
        cont_field = {"conferencePaper": "proceedingsTitle", "bookSection": "bookTitle"}.get(it["type"], "publicationTitle")
        fill = {k: v for k, v in {cont_field: s["container"], "pages": s["pages"], "volume": s["volume"], "issue": s["issue"],
                                  "date": s["date"]}.items() if v and not f.get(k) and not (k in ("volume", "issue", "publicationTitle") and it["type"] in ("preprint", "report", "thesis", "book"))}
        if fill:
            out.append({"check": "empty_fields_fillable", "fill": fill})
        return out
    return discover(it, src)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crossref", action="store_true")
    ap.add_argument("--library")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--db", default=os.path.expanduser("~/Zotero/zotero.sqlite"))
    a = ap.parse_args()
    if not os.path.exists(a.db):
        print(json.dumps({"error": f"database not found: {a.db}"}))
        return
    try:
        c, tmp = snapshot(a.db)
    except sqlite3.Error as e:
        print(json.dumps({"error": f"snapshot failed: {e}"}))
        return
    try:
        libs = libraries(c)
        lib_filter = None
        if a.library:
            lib_filter = next((i for i, n in libs.items() if a.library in (str(i), n)), -1)
            if lib_filter == -1:
                print(json.dumps({"error": f"unknown library {a.library}", "libraries": libs}))
                return
        items = load_items(c, lib_filter)
        if a.limit:
            items = items[:a.limit]
        cr = Sources() if a.crossref else None
        year = date.today().year
        findings = []
        for it in items:
            fs = local_checks(it, year) + (crossref_checks(it, cr) if cr else [])
            if fs:
                findings.append({"key": it["key"], "library": libs.get(it["library"], it["library"]), "type": it["type"],
                                 "title": (it["f"].get("title") or "")[:120], "doi": it["doi"], "findings": fs})
        counts = defaultdict(int)
        for x in findings:
            for f in x["findings"]:
                counts[f["check"]] += 1
        print(json.dumps({"libraries": libs, "items_scanned": len(items), "crossref": bool(cr),
                          "crossref_failures": cr.errors if cr else 0,
                          "semantic_scholar_disabled": cr.s2.disabled if cr else None, "counts": dict(sorted(counts.items())),
                          "duplicates": duplicate_groups(items), "items": findings}, ensure_ascii=False, indent=1))
    finally:
        c.close()
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
