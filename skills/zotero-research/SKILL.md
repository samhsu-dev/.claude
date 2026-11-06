---
name: zotero-research
description: Survey, curate, and enrich a Zotero library for a research topic — reconcile a .bib, organize collections, normalize tags, attach markdown, and write summary notes. Use when the user asks to research a field in Zotero, organize a library, or import/summarize references.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
argument-hint: "[library name or group id, optional .bib path, optional topic focus]"
---

Curate and enrich a Zotero library for a research domain. Operate on the library named or implied by `$ARGUMENTS`. The work spans reconciling references, organizing collections, normalizing tags, attaching full-text markdown, and writing summary notes.

This skill writes to a shared Zotero library. Treat every write as high-blast-radius. Verify ground truth before acting, checkpoint before bulk writes, and never trust a single listing tool as authoritative.

## Prerequisites

1. The `zotero` MCP server is connected. If its tools are absent, tell the user to configure it and stop.
2. Zotero desktop is running with the local API enabled (Settings → Advanced → "Allow other applications…"). Confirm with `curl -s -o /dev/null -w "%{http_code}" http://localhost:23119/connector/ping` → expect `200`. `pgrep Zotero` is unreliable; trust the API probe.
3. Writes (notes, tags, attachments, item edits) require a Web-API key with library + file + write permission. The local API is read-capable but does NOT support file uploads.
4. Read `${CLAUDE_SKILL_DIR}/reference.md` for the API key/env-file convention and the file-upload protocol before any write.

## Step 1 — Establish ground truth (READ ONLY)

Never trust `zotero_get_recent` or any single MCP listing as a complete inventory — it has been observed to omit existing items, causing duplicate creation.

1. `zotero_list_libraries` → find the target library ID. `zotero_switch_library` to it. Re-run the switch after any session reset; the MCP silently reverts to the default library.
2. Pull the authoritative item list from the local API, not the MCP:
   `curl -s "http://localhost:23119/api/groups/<GID>/items/top?limit=100&format=json"` (use `/users/0/` for the personal library).
3. `zotero_get_collections` → record collection keys (the MCP `collections` arg needs 8-char KEYS, not names — names fail).
4. `zotero_find_duplicates` (method `doi` or `both`) → record candidate groups. Do NOT merge yet.
5. If a `.bib` was given, read it and cross-check every entry against the API inventory by title + DOI. Classify each as already-present vs genuinely-missing. Most "missing" entries are usually already present under a different key.

Report the audit before writing: item count, collections, duplicates, and the true missing-vs-present breakdown.

## Step 2 — Reconcile references (WRITE — checkpoint first)

For entries genuinely absent from the library:

- DOI present → `zotero_add_by_doi(doi, collections=[<KEY>], attach_mode='none' or 'auto')`.
- arXiv only / DOI not on CrossRef → `zotero_add_by_url('https://arxiv.org/abs/<id>')`. The arXiv path ignores the `collections` arg — file it afterward with `zotero_manage_collections`.
- Title-only stub (no DOI/URL/author) → do NOT add; report it as unresolvable.

Add ONE item first, verify it landed correctly, then batch the rest.

## Step 3 — Organize collections (WRITE)

- Map each top-level item to topic collections from the API `collections` field (ground truth), not a guess.
- File uncategorized items with `zotero_manage_collections(item_keys=[...], add_to=[<KEY>])`.
- Create new collections only when an existing one does not fit.

## Step 4 — Normalize tags (WRITE)

1. `zotero_get_tags` → inspect the current vocabulary. Expect inconsistency: mixed casing, arXiv category cruft (`Computer Science - …`), single-paper keywords, junk like `⛔ No DOI found`.
2. Design a controlled vocabulary with `prefix:value` namespaces (Zotero's flat-tag convention), e.g. `topic:`, `method:`, `type:`. Confirm the namespace plan and the fate of old tags with the user (keep / clean junk only / full replace).
3. Apply per item. `zotero_update_item(item_key, tags=[...])` REPLACES the whole tag list — on full-replace this also evicts orphaned old tags automatically. Use `add_tags`/`remove_tags` for incremental edits.

## Step 5 — Attach full-text markdown (WRITE)

Markdown conversion is pure and free — `markitdown` is programmatic, costs zero tokens. Do NOT read PDFs through the model to convert them.

1. Map each parent item → its PDF attachment key + local path via the API attachments query (see `reference.md`). Verify each file exists on disk.
2. Convert: `markitdown "<pdf>" -o "<same-name>.md"`. Install once if missing: `uv tool install 'markitdown[all]'`.
3. Skip HTML-snapshot-only items where the snapshot is a paywall/nav page — conversion yields junk. Inspect the first ~40 lines before trusting output.
4. Attach each `.md` as a child of its parent via the Web API using the helper:
   `${CLAUDE_SKILL_DIR}/scripts/zotero_attach_md.py <parent_item_key> <abs_md_path>`
   It is idempotent (skips if an `.md` child already exists) and prints a JSON-ish status line per file.
5. The MCP children view caches; verify attachments via the API, not `zotero_get_item_children`.

## Step 6 — Write summary notes (WRITE — sample first)

Summaries need only abstract + introduction, not full text. Pull abstracts from the `.bib` and/or the converted markdown; read only the intro slice when an abstract is missing.

1. Compose one summary, create it with `zotero_create_note`, and STOP for the user to review format/depth before batching.
2. Note template (single heading — Zotero uses the first line as the note title; do not add a duplicate `<h1>`):
   - `<h2>Summary — {Title}</h2>`
   - `<p><strong>Venue:</strong> {venue · authors}</p>`
   - `<p><strong>Problem.</strong> …</p>` `<p><strong>Approach.</strong> …</p>` `<p><strong>Evaluation.</strong> …</p>`
   - `<p><strong>Relevance to {topic}.</strong> …</p>`
   - `<p><em>Generated from abstract + introduction. …</em></p>`
3. Grey literature (vendor whitepapers, blogs, news, repos) → a lightweight note: type, one-paragraph gist, relevance. Label it as grey literature, not an academic source.
4. Cross-reference preprint/published twins in each other's notes.

## Step 7 — Verify (READ ONLY)

Run a coverage pass over the API top-level list: for each item confirm tags present, markdown attachment present (where a PDF existed), and a summary note present. Report gaps and close them. Confirm the old tag vocabulary is gone via `zotero_get_tags`.

## Safety rules

- Re-`zotero_switch_library` after any session reset before writing.
- Verify against the local API, never a single MCP listing.
- Checkpoint before Step 2 and before the Step 6 batch.
- Deletions go to Trash (recoverable); still get explicit user approval before deleting in a shared library. Never empty the Trash.
- If you create an erroneous write, revert it transparently and tell the user — do not paper over it.
- Never write the API key into SKILL.md, scripts, or any committed file. Read it from the user's env file at run time.

## Error handling

| Symptom | Cause | Action |
|---------|-------|--------|
| `No item found with key` on write | MCP reverted to default library | Re-run `zotero_switch_library`. |
| `not a valid collection key` | passed a name, not a key | Use the 8-char key from `zotero_get_collections`. |
| `DOI not found on CrossRef` (arXiv DOI) | arXiv DOIs absent from CrossRef | Use `zotero_add_by_url` with the arXiv abs URL. |
| upload 403 / quota | Zotero cloud file quota | Metadata still lands; report the failed file. |
| markitdown junk output | HTML snapshot is a paywall page | Skip the attachment; still write a summary from the abstract. |
