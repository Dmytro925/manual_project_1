---
name: api-functional-test-cases
description: Use when asked to design, generate, or update manual API functional test cases for a e-store endpoint, or to re-verify existing case expectations against the live test environment.
---

# API functional test cases

Turn one REST API endpoint into a review-ready set of manual test cases destined for TTGO, where every expected result is backed by a verified live response.

## Steps

1. **Gather prior state and spec.** Read `docs/test-cases/TRACKER.md` — the endpoint's row carries reusable verified facts (`setup only` with notes means part of its contract is already probed) — and skim the existing case documents in `docs/test-cases/`: they hold verified auth shapes, working setup chains, and recurring deviations. Then fetch the endpoint section plus its FR requirements and the error tables from the [spec sources](#spec-sources). Done when you hold: request/response contract, documented error codes and statuses, auth requirements, validation rules, and the list of facts prior documents already verified.
2. **Design cases.** Apply the [case standard](#case-standard). Cover the happy path, each documented error variant, role/auth variants, and field-validation variants. Assign IDs in the endpoint family's prefix, continuing numbering from the cases published in TTGO (check with `ttgo search <PREFIX> -o json`) and from the working copies in `docs/test-cases/`; a published ID is permanent. Done when every requirement branch of the endpoint section is covered by a case or listed under "Out of scope" in the document.
3. **Verify live.** Probe every case, negatives included, with `uv run python` + `requests` (or curl) against the [environment](#environment). Build precondition state through the documented setup chain; use a fresh disposable `X-Session-ID` UUID per flow and record every record you create. Clean up through the APIs that allow it (clear carts, revert stock or status you changed); on destructive endpoints, act only on resources this probe run created. When a probe answer changes between calls, re-probe and record the instability in Appendix B. Expected results state the verified actual response. Where reality and spec disagree, keep reality in the case and record the deviation for Appendix B. Done when every expected result in every case traces to a recorded response and no unverified expectation remains.
4. **Write the document** to `docs/test-cases/<endpoint-slug>.md` (a gitignored working copy): header table (environment, verification date, spec sources, sensitive-data note), Conventions, cases, then Appendix A traceability (case → FR-xxx), Appendix B deviations (documentation vs live environment — reference a deviation already recorded in a sibling document instead of restating it; record only new ones), Appendix C verification log (method, created data, tooling, date). Done when a tester can execute every case using only the document and the environment.
5. **Publish to TTGO** only when asked, following the `ttgo-case-migration` skill (folder/category mapping, credential inlining, and the intended-behavior policy for deviations). The repo working copy keeps placeholders.
6. **Update the coverage tracker** (`docs/test-cases/TRACKER.md`) only when the user asks, and only after the case document passed live verification and its details were agreed with the user: set the endpoint's status, case document with its ID prefix, verification date, and any new Notes, then recompute the summary line.

## Case standard

```
ID: <PREFIX>-<NNN>
Title: short, names the check, no status codes
Description: self-contained — states what must happen, no external reading required;
  "Trace: FR-xxx" references go last
Preconditions: (optional) declarative state; a setup chain in parentheses is an
  automation hint, not steps
Steps:
  1. one request to the endpoint under test, exact method/path/body
     - HTTP status;
     - every asserted response field or error detail (one or more per step).
Category: API / Functional / [Admin /] <Module> / <Positive|Negative>
```

- One test case has exactly one endpoint under test; extra steps are input variations of the same request.
- Every step has ≥1 expected result; an expected result never exists without a step.
- Assert only the stable contract: no exact account/order IDs, no environment-dependent fields.
- Case text is English. Sensitive values stay placeholders in the repo copy.
- Prefix = short endpoint-family token (e.g. `LOGIN`, `OSTAT`); the functional module lives in the Category.
- The `Admin` category marker is mandatory when the endpoint under test is admin-only or the case performs its steps under test as admin (e.g. `API / Functional / Admin / Orders / Negative`). Admin used only to prepare or clean up state leaves the Category plain.
- Teardown and corroboration steps are allowed inside a case when labeled as such ("cleanup", "corroboration"); they never become the subject under test — the case still has exactly one endpoint under test.
- Repeated request bodies and response contracts may be defined once above the cases as named building blocks (e.g. a valid checkout body, a 201 success contract) and referenced by name from expected results.

## Environment

- Base URL `https://e-shop.dev.aqa-lab.space`, API prefix `/api`.
- Credentials come from the root `.env` / `config/environments.py` getters at probe time; the admin password is `$Admin` + current `DDMMYYYY` (`get_admin_user` rule).
- Treat everything a probe returns as potentially sensitive: truncate tokens in output, never paste real values into the document.

## Spec sources

- `https://raw.githubusercontent.com/Mani-QA/ecommerce/main/docs/REST-API-DOCUMENTATION.md` — request/response contract, endpoints, error tables.
- `https://raw.githubusercontent.com/Mani-QA/ecommerce/main/docs/FRD-QADemo.md` — functional requirements (`FR-xxx`), user roles, validation rules.
