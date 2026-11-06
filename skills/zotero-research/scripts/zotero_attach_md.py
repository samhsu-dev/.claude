#!/usr/bin/env python3
"""Attach a local file as a child 'imported_file' attachment to an existing
Zotero item, via the Zotero Web API (api.zotero.org).

Usage: zotero_attach_md.py <parent_item_key> <absolute_file_path>

Env:
  ZOTERO_API_KEY  (required) Web API key with library + files + write perms.
  ZOTERO_GROUP_ID (default 0) group id; 0 targets the personal (user) library.

Implements the 4-step Zotero upload: create item -> request upload auth ->
POST bytes to storage -> register upload. Idempotent: skips if the parent
already has an .md attachment. Prints one status line; never crashes the caller.
"""
import hashlib
import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request

API = "https://api.zotero.org"
KEY = os.environ.get("ZOTERO_API_KEY")
GROUP = os.environ.get("ZOTERO_GROUP_ID", "0")
if GROUP and GROUP != "0":
    BASE = f"{API}/groups/{GROUP}"
else:
    LIB = os.environ.get("ZOTERO_LIBRARY_ID", "")
    BASE = f"{API}/users/{LIB}"


def req(method, url, data=None, headers=None, raw=False):
    h = {"Zotero-API-Version": "3", "Authorization": f"Bearer {KEY}"}
    if headers:
        h.update(headers)
    body = data
    if data is not None and not raw:
        body = json.dumps(data).encode()
        h.setdefault("Content-Type", "application/json")
    r = urllib.request.Request(url, data=body, method=method, headers=h)
    with urllib.request.urlopen(r) as resp:
        return resp.status, resp.read(), dict(resp.headers)


def existing_md_child(parent):
    try:
        _, raw, _ = req("GET", f"{BASE}/items/{parent}/children")
    except Exception:
        return None
    for it in json.loads(raw):
        d = it.get("data", {})
        if d.get("itemType") == "attachment" and d.get("filename", "").endswith(".md"):
            return d.get("filename")
    return None


def main():
    if not KEY:
        print("FAIL: ZOTERO_API_KEY not set")
        return
    if len(sys.argv) != 3:
        print("FAIL: usage zotero_attach_md.py <parent_key> <abs_path>")
        return
    parent, path = sys.argv[1], sys.argv[2]
    if not os.path.isabs(path) or not os.path.exists(path):
        print(f"FAIL {parent}: file not found ({path})")
        return
    fname = os.path.basename(path)

    already = existing_md_child(parent)
    if already:
        print(f"SKIP {parent}: md attachment already exists ({already})")
        return

    try:
        raw_bytes = open(path, "rb").read()
        md5 = hashlib.md5(raw_bytes).hexdigest()
        filesize = len(raw_bytes)
        mtime = int(os.path.getmtime(path) * 1000)
        ctype = mimetypes.guess_type(path)[0] or "text/markdown"

        # 1) create attachment item
        _, tmpl_raw, _ = req(
            "GET", f"{API}/items/new?itemType=attachment&linkMode=imported_file"
        )
        tmpl = json.loads(tmpl_raw)
        tmpl.update({
            "parentItem": parent, "title": fname, "filename": fname,
            "contentType": ctype, "charset": "utf-8",
        })
        _, raw, _ = req("POST", f"{BASE}/items", data=[tmpl])
        res = json.loads(raw)
        if res.get("failed"):
            print(f"FAIL create {parent}: {res['failed']}")
            return
        attach_key = res["successful"]["0"]["key"]

        # 2) request upload authorization
        form = urllib.parse.urlencode({
            "md5": md5, "filename": fname, "filesize": filesize, "mtime": mtime,
        }).encode()
        _, raw, _ = req(
            "POST", f"{BASE}/items/{attach_key}/file", data=form, raw=True,
            headers={"Content-Type": "application/x-www-form-urlencoded",
                     "If-None-Match": "*"},
        )
        auth = json.loads(raw)
        if auth.get("exists") == 1:
            print(f"OK {parent}: file already on server -> {attach_key}")
            return

        # 3) upload bytes to storage
        upload_body = auth["prefix"].encode() + raw_bytes + auth["suffix"].encode()
        up = urllib.request.Request(
            auth["url"], data=upload_body, method="POST",
            headers={"Content-Type": auth["contentType"]},
        )
        with urllib.request.urlopen(up) as resp:
            if resp.status not in (200, 201):
                print(f"FAIL storage upload {parent}: {resp.status}")
                return

        # 4) register the upload
        reg = urllib.parse.urlencode({"upload": auth["uploadKey"]}).encode()
        status, _, _ = req(
            "POST", f"{BASE}/items/{attach_key}/file", data=reg, raw=True,
            headers={"Content-Type": "application/x-www-form-urlencoded",
                     "If-None-Match": "*"},
        )
        print(f"OK {parent}: attached {fname} -> {attach_key} (status {status})")
    except Exception as e:
        print(f"FAIL {parent}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
