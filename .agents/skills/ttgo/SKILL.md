---
name: ttgo
description: Use when the user asks to interact with TTGO - manage test cases, test runs, requirements, analytics, defects, categories, backups, webhooks, AI generation, or any test management operation via the ttgo CLI
---

# TTGO CLI Skill

You are a QA operator managing the TTGO test management system via the `ttgo` CLI tool.

## Prerequisites

Before running any command, verify the CLI is configured:

1. Run `ttgo config show` to check the current configuration
2. If no server URL or token is set, ask the user for:
   - Server URL (default: http://localhost:8080)
   - API token (create one in TTGO Settings > API Tokens)
3. Configure with `ttgo config set-server <url>` and `ttgo config set-token <token>`

## Conventions

- **Always** use `--output json` (`-o json`) for machine-readable output you need to parse
- Parse JSON responses to extract IDs, statuses, and relevant data for follow-up commands
- When creating resources, capture and report the returned ID to the user
- Use `ttgo search <query>` to resolve human-readable names to IDs when the user refers to things by name
- For list commands, use `--limit` and `--offset` for pagination where supported (not every list command has them — check `--help` first)

## Available Command Domains

Run `ttgo --help` to see all commands. Run `ttgo <command> --help` for subcommand details.

| Domain | Command | Description |
|--------|---------|-------------|
| Config | `ttgo config` | show, set-server, set-token |
| Tests | `ttgo tests` | list, get, create, update, steps, delete, versions, restore, executions |
| Folders | `ttgo folders` | tree, get, create, rename, move, delete |
| Runs | `ttgo runs` | list, get, create, complete, reopen, copy, delete |
| Results | `ttgo runs results` | add, update, retry, bulk-update, delete |
| Search | `ttgo search` | Full-text search across tests, requirements, runs |
| Categories | `ttgo categories` | list, create, delete, assign |
| Requirements | `ttgo requirements` | list, get, create, update, delete, link, unlink, import, bulk-import, resync, post-to-jira |
| Analytics | `ttgo analytics` | summary, trend, flaky, most-failed, duration, duration-top, component-health, growth, passing-rate, unique-bugs, activity, compare-runs |
| Defects | `ttgo defects` | list, link, unlink, create-issue |
| Backups | `ttgo backups` | list, create, restore, delete, schedule get/set |
| Webhooks | `ttgo webhooks` | list, create, delete |
| AI | `ttgo ai` | providers (list/create/test/set-default/delete), generate, accept, template (get/set/reset), compare, typesafe (get/set/test), features (get/set) |
| Users | `ttgo users` | list, create, update, delete, restore |

## Workflow Examples

### Create a test case with steps
```bash
# 1. Create the test case (no steps flag — keep it simple)
ttgo tests create --name "Login works" --folder <folder-id> -o json   # returns the id

# 2. Attach all steps in one replace-all request
ttgo tests steps <test-id> --steps '[{"action":"Open login page","expected_result":"Form is shown"},{"action":"Submit valid credentials","expected_result":"Dashboard opens"}]' -o json
```
A step is `{"action": "...", "expected_result": "...", "id": "...", "order_index": 0}`;
`id` and `order_index` are optional (`order_index` defaults to the array position).

### Edit steps of an existing test — read all, modify, send all back
`ttgo tests steps` replaces the whole step list, so every edit (add, remove,
reorder, change one step) is: fetch the array, modify it, send it back in full.
```bash
ttgo tests get <test-id> -o json | jq '.steps' > steps.json   # edit steps.json (keep existing ids)
cat steps.json | ttgo tests steps <test-id> --steps-file - -o json
```
A broken payload replaces the list just as readily as a good one — malformed
fields silently become empty steps. So treat the file as a checkpoint: validate
every step still has content (`jq -e 'all(.[]; .action != null and .action != "")' steps.json`)
before sending, and send the validated file, never an inline `--steps "$(jq ...)"`.
Pass `--steps '[]'` to remove every step.

### Safe step editing — prefer `scripts/steps-edit.sh`
For remove/insert/move/set edits prefer the helper script. It anchors every
position to a step **id** (never a numeric array index), separates editing
from sending, and refuses stale or foreign checkpoints:

```bash
scripts/steps-edit.sh show <test-id>                                  # current steps, numbered (with full ids)
scripts/steps-edit.sh edit <test-id> remove --id <step-id>
scripts/steps-edit.sh edit <test-id> insert --before <anchor-step-id> --action "..." --expected "..." [--id <step-id>]
scripts/steps-edit.sh edit <test-id> move   --id <step-id> --after <anchor-step-id>
scripts/steps-edit.sh edit <test-id> set    --id <step-id> --action "..." --expected "..."
scripts/steps-edit.sh send <test-id>                                  # sends the reviewed ./steps-edited.json
```

Step ids are printed **in full** and must be passed in full: copy the whole id
from `show` into `--id`/`--before`/`--after`. A partial or wrong id is refused
with the ids the test actually has, and the list a step was inserted into
carries `new step — id assigned on send` until the server gives it one.

`edit` never touches the server: it writes `steps-edited.json` + `.meta`
sidecars under `$TTGO_STEPS_DIR` (default `$TMPDIR/ttgo/`, never the repo)
and prints the resulting numbered list. Compare that list against
what was asked for BEFORE sending. `send` re-validates and aborts if the
checkpoint was made for a different test or the server changed since it was
fetched. `--id` on insert reuses an existing step id (restoring a deleted step).

When hand-rolling jq instead of the script: express every position relative to
a step `id`, never a numeric array index, and print the final ordered list
(`jq -r 'to_entries[] | "\(.key + 1). \(.value.action)"'`) and verify it
against the intended order before sending.

### Run smoke tests and report results
```bash
# Find the smoke category
ttgo categories list -o json | jq '.categories[] | select(.name | test("smoke"; "i"))'

# Create a new run
ttgo runs create --name "Smoke Run $(date +%Y-%m-%d)" --category <category-id> -o json

# For each test case, add results
ttgo runs results add <run-id> --test <test-id> --status PASS -o json
ttgo runs results add <run-id> --test <test-id> --status FAIL --error "Login button not found" -o json

# Complete the run
ttgo runs complete <run-id>
```

### Find flaky tests and investigate
```bash
# Get flaky tests
ttgo analytics flaky -o json

# Get details on a specific flaky test
ttgo tests get <test-id> -o json
ttgo tests executions <test-id> -o json
```

### Import requirements and generate tests
```bash
# Import from Jira
ttgo requirements import --source jira --key PROJ-123 -o json

# Generate tests from the requirement
ttgo ai generate --requirement <req-id> --coverage thorough -o json

# Accept the generated tests
ttgo ai accept --requirement <req-id> -o json
```

### Link a defect to a failed test result
```bash
# Find the failed result in a run
ttgo runs get <run-id> -o json | jq '.run_results[] | select(.status == "FAIL")'

# Link a Jira defect
ttgo defects link --run <run-id> --result <result-id> --jira-key BUG-456
```

## Error Handling

- If a command fails, read the error message from stderr
- Common errors:
  - "cannot connect to TTGO server" -- server is not running
  - "authentication failed" -- token is invalid or expired
  - "permission denied" -- admin operation attempted with non-admin token
  - "not found" -- resource ID is incorrect, use `ttgo search` to find the right one
