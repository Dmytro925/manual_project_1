---
name: ttgo-case-migration
description: Use when asked to publish, migrate, or continue migrating manual test cases from docs/test-cases/ working copies into TTGO — folder/category mapping, credential inlining, and intended-behavior decisions for cases whose live behavior deviates from the documented contract.
---

# TTGO case migration

Turn a verified case document (`docs/test-cases/<slug>.md`) into permanent TTGO cases. The md document records **actual** live behavior; TTGO cases assert **intended** behavior. Cases whose expectations rest on a defect get transformed, never copied.

Reaching for: `ttgo` skill (CLI commands), `api-functional-test-cases` skill (case standard, environment, spec sources).

## Steps

1. **Survey.** Read the full case document — appendices included — `docs/test-cases/TRACKER.md`, and the live TTGO state (`ttgo config show`; `ttgo folders tree`, `ttgo categories list`, `ttgo search <PREFIX>` to catch a partially migrated set — published IDs are permanent, so keep them). Classify every Appendix B deviation as **defect candidate** (assert the documented contract) or **outdated doc / spec clarification / quirk** (assert the verified reality). Done when every case carries a keep-or-transform decision and every deviation a classification.
2. **Settle decisions.** Present the user a per-case table: folder, categories, and each transform with the exact assertion level — where the docs omit the precise code/message of the correct behavior, propose one (e.g. "HTTP 4xx, no order created"). Await explicit approval of every flagged decision before writing to TTGO. Done when all flagged decisions are answered.
3. **Create the structure.** Folders `Manual/API/<Module>` / `Manual/UI/<Module>`; categories as flat names per [mapping](#case-mapping). Create only what is missing. Done when the live tree matches the approved mapping.
4. **Generate payloads** with the [mechanics](#mechanics). Done when every steps file passes the jq gate and no secret value left `$TMPDIR/ttgo/`.
5. **Publish and verify.** Per case: create → steps → category assign. Then re-read the live state (`ttgo tests list -o json`) and compare name, folder, categories, and step count of every case against the approved table. Done when they match.
6. **Report** per-case what changed versus the md — title, description, steps — claiming only what the live TTGO state confirms, and which published cases will FAIL until a defect is fixed. Update `docs/test-cases/TRACKER.md` only when the user asks. Done when every claim in the report matches the live state of the case it describes.

## Case mapping

- **Name:** `<PREFIX>-<NNN>: <md title>` — the md ID is the permanent case ID; the TTGO UUID stays an internal detail.
- **Categories:** flat names, a test carries several. The document's `API / Functional / [Admin /] <Module> / <Positive|Negative>` becomes the words `API` (UI sets use `UI`), `Functional`, optionally `Admin` (admin-only endpoint or the case acts as admin in its steps under test), the module, `Positive` / `Negative`. Resolve IDs with `ttgo categories list -o json`; create missing ones.
- **Folder:** the resource module — admin order cases sit in `Manual/API/Orders`, not an `Admin` folder; the `Admin` category carries the marker.
- **Description (HTML):** one `<p>` of case substance ending with `Trace: FR-xxx`, then one `<p><b>Preconditions:</b> …</p>`. Self-contained: when the md defines a shared building block (checkout chain, loaded session), inline it into the precondition that uses it, with real credentials kept. The description holds only substance and preconditions — environment/base-URL lines go stale, and defect notes belong to the engineer who files them.
- **Steps:** HTML (`<code>`, `<ul><li>`, `<b>`); one action plus a single `expected_result` whose `<li>` items are the assertions; API paths stay relative (`/api/…`). Keep `corroboration` / `cleanup` labels. A shared response contract (the 201 success contract) expands in full into the `expected_result` of every step that asserts it — a step never cross-references another section of the case, so each step stays individually pass/fail-able at field level.
- **Credentials:** inline real values (TTGO storage is access-controlled). Read them at payload-generation time from the `config/environments.py` getters (`get_standard_user`, `get_locked_user`, `get_admin_user`); keep secrets out of chat, repo files, and script output. Dynamic values keep their formula: admin password is written `$Admin<DDMMYYYY of the current date>`, so it never goes stale; a Basic header for a date-derived account keeps the formula inside the placeholder (`Basic <base64 of admin_user:$Admin<DDMMYYYY of the current date>>`) — never pre-encode a dated password.

## Intended behavior

A defect-candidate deviation becomes an assertion of the **documented** contract; the case FAILs until the fix, and that red state is the suite doing its job — the automation engineer files and links the defect, not the case text.

A transform rewrites the case's whole identity to the intended behavior: retitle when the md title celebrated the deviation (the `PREFIX-NNN` stays), phrase every description sentence as what must happen, and drop corroboration steps that only make sense against the buggy behavior (e.g. reading back an order that, in the intended contract, is never created).

Transformation classes approved in earlier sets (LOGIN, OSTAT, CHK):

| md recorded reality | TTGO asserts |
| --- | --- |
| schema errors answer `ZodError` + `error.issues[]` (login, admin status, checkout) | FR-ERR-001 shape: 400, `error.code = "VALIDATION_ERROR"`, `error.message = "Validation failed"`, non-empty `error.details.<field>` entry per offending field |
| login returns no `refreshToken` | `data.refreshToken` is a non-empty string |
| locked account still authenticates on some path (e.g. checkout via Basic) | the request is refused with HTTP 403 |
| declined test card accepted; past `expiryDate` accepted | refused — approved level: HTTP 4xx, `success = false`, no `data`, no order (exact code undocumented — settle with the user per case) |
| non-admin Bearer denial answers 401 `UNAUTHORIZED` / "Invalid token" | 403 `FORBIDDEN`, `error.message = "Admin access required"` |

Reality-OK classes keep the verified actual result: `userType = "standard"`; `"Cart is empty"`; advisory order-lifecycle transitions (any enum value accepted); signup rejecting reserved email domains; missing `X-Session-ID` surfacing as `CART_EMPTY`; `HTTP_ERROR` / `"Malformed JSON in request body"`.

## Mechanics

Generate payloads inside the project environment so credentials come from `.env` — a Python script importing `config.environments`, run as `PYTHONPATH=. uv run python <script>`, writing per case `<id>.name`, `<id>.desc`, `<id>.steps.json`, `<id>.cats` (one category UUID per line) under `$TMPDIR/ttgo/`; the script prints only file paths. Never generate payloads in the repo.

Validate before sending (a broken payload silently replaces good steps):

```bash
jq -e 'all(.[]; .action != null and .action != ""
  and .expected_result != null and .expected_result != "")' "$f.steps.json"
```

Publish per case (`"$(cat …)"` keeps a literal `$Admin` in descriptions):

```bash
id=$(ttgo tests create --name "$(cat "$f.name")" --folder <folder-id> \
      --description "$(cat "$f.desc")" -o json | jq -r .id)
ttgo tests steps "$id" --steps-file "$f.steps.json" -o json
while read -r cat; do
  ttgo categories assign --test "$id" --category "$cat" -o json
done < "$f.cats"
```
