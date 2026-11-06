# Zotero Web API reference

Read on demand. Details the credential convention and the API calls the skill relies on.

## Credentials

The Web API key + library id live in a user env file (convention: `~/.config/zotero-mcp.env`), sourced at run time. Never hard-code or commit the key.

```bash
set -a; . ~/.config/zotero-mcp.env; set +a
```

Expected vars: `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID`, `ZOTERO_LIBRARY_TYPE`, `ZOTERO_LOCAL`.

The key needs group `write` + `files` permission for uploads. Verify:

```bash
curl -s "https://api.zotero.org/keys/$ZOTERO_API_KEY" | python3 -m json.tool
```

## Local vs Web API

| Capability | Local API (`localhost:23119`) | Web API (`api.zotero.org`) |
|------------|-------------------------------|----------------------------|
| Read items/collections | yes (fast, offline) | yes |
| File upload (attach md) | NO (template 404) | yes |
| Requires Zotero running | yes | no |

Use the local API for ground-truth reads; the Web API for file uploads.

## Ground-truth queries

Group library `<GID>` (use `/users/0/` for the personal library in local mode):

```bash
# all top-level items
curl -s "http://localhost:23119/api/groups/<GID>/items/top?limit=100&format=json"

# every attachment (map parent -> pdf key -> filename)
curl -s "http://localhost:23119/api/groups/<GID>/items?limit=150&format=json&itemType=attachment"
```

A PDF attachment's local path is:
`/Users/<user>/Zotero/storage/<ATTACHMENT_KEY>/<filename>`

Filter PDF attachments in Python: `contentType == 'application/pdf'` and `linkMode in ('imported_file','imported_url')`. `linked_url` attachments (e.g. ResearchGate links) have no local file — skip them.

## File-upload protocol (4 steps)

The attach script implements this; documented here for reference. All against `https://api.zotero.org/groups/<GID>`:

1. `GET /items/new?itemType=attachment&linkMode=imported_file` → template; set `parentItem`, `title`, `filename`, `contentType`, `charset`. `POST /items` (array) → attachment key.
2. `POST /items/<key>/file` with `md5,filename,filesize,mtime` form body + header `If-None-Match: *` → upload auth (`url`, `prefix`, `suffix`, `contentType`, `uploadKey`). If `exists==1`, file already on server — done.
3. `POST` to the storage `url` with body `prefix + filebytes + suffix` and `Content-Type` from auth.
4. `POST /items/<key>/file` with `upload=<uploadKey>` + `If-None-Match: *` → registers the file.

Headers on every API call: `Zotero-API-Version: 3`, `Authorization: Bearer <key>`.

## Script

`scripts/zotero_attach_md.py <parent_item_key> <abs_file_path>`

- Reads `ZOTERO_API_KEY` from env; group id from `ZOTERO_GROUP_ID` (export before calling).
- Idempotent: skips if the parent already has an `.md` attachment.
- Prints one status line per file (`OK …` / `SKIP …` / `FAIL …`).

Driver example for many files:

```bash
set -a; . ~/.config/zotero-mcp.env; set +a; export ZOTERO_GROUP_ID=<GID>
python3 -c "
import glob, subprocess
M={'PARENTKEY':'PDFATTACHKEY', ...}
for parent,key in M.items():
    mds=glob.glob(f'/Users/<user>/Zotero/storage/{key}/*.md')
    if not mds: print('NO MD', parent); continue
    r=subprocess.run(['python3','${CLAUDE_SKILL_DIR}/scripts/zotero_attach_md.py',parent,mds[0]],capture_output=True,text=True)
    print((r.stdout+r.stderr).strip())
"
```
