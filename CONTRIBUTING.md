# Contributing

Start with [README.md](README.md) for setup and commands, then read [CODING_STANDARDS.md](CODING_STANDARDS.md) before changing code. This document owns the contribution workflow, including Git commits and pull requests; no separate Git-rules file is needed.

## Scope and branches

1. Read the issue, its comments, and acceptance criteria before implementation. Ask about unclear requirements. If a better solution differs from the requested implementation, explain the deviation and its behavior impact.
2. Start from an up-to-date `main`. For issue work, follow the current branch convention: `feat/issue_<number>`. For small work without an issue, use a descriptive branch such as `docs/<short-description>`, `fix/<short-description>`, or `chore/<short-description>`.
3. Keep one coherent purpose per PR. Separate unrelated improvements into follow-up work. A naming, import, annotation, or documentation refactor should preserve test behavior, assertions, and expectations unless the issue explicitly asks to change them.
4. Keep commits focused and independently understandable. Commit dependency declarations and their `uv.lock` changes together. Review the final diff for accidental deletions, unrelated formatting, secrets, and generated files.
5. Merge changes into `main` through a PR rather than pushing directly. Keep `gh-pages` for generated reports; it is not a source-code branch.

## Documentation maintenance

Keeping documentation current is part of completing a task, not a separate cleanup phase. For every change, assess its documentation impact and update affected guidance and examples in the same task/PR as the implementation.

| What changes | Documentation to review |
| --- | --- |
| Setup, commands, environment variables, meaningful test coverage/layout changes, reports, or CI behavior | `README.md` |
| Coding, naming, import, fixture, test-design, or architecture conventions | `CODING_STANDARDS.md` |
| Contribution or verification workflow | `CONTRIBUTING.md` and the PR template, as applicable |
| Agent instructions or paths/responsibilities in the working map | `AGENTS.md` |

Document contributor-facing behavior and important structural changes rather than maintaining an inventory of every class or test. Adding an internal method or test does not automatically require a README edit if the existing guidance remains accurate.

Before handoff or review, check affected paths, commands, examples, and coverage claims against the implementation. Replace or remove obsolete instructions and resolved caveats rather than appending conflicting advice. Describe implemented capabilities as current behavior; clearly label planned work separately.

Record the documentation impact in the PR body or task handoff: list the updated files, or state that no update was needed and briefly explain why. Reviewers should check this alongside code and test results.

## Commit messages

For new work, use a lightweight Conventional Commits format:

```text
type(optional-scope): imperative summary
```

Use `feat` for new framework capability, `fix` for a defect, `test` for test coverage, `refactor` for behavior-preserving restructuring, `docs` for documentation, `ci` for workflows, and `chore` for maintenance/tooling.

Examples:

```text
test(auth): cover rejected login attempts
fix(pages): use the navbar sign-in locator
refactor(api): import base clients from concrete modules
docs: document local setup and contribution workflow
ci: preserve test artifacts after failures
```

- Write short, specific English subjects. Name the change rather than using only an issue/task number or a vague subject such as “fixes after review”.
- Add a body when the reason, tradeoff, or behavior change is not clear from the subject. Reference the relevant issue with `Refs #<number>` when applicable.
- Inspect the staged changes before committing. Include code, relevant tests, and documentation for the same logical change; leave unrelated work out.
- This format is a convention for new work, not a commit-message CI gate or a requirement to rewrite historical commits. Keep Git's generated merge/revert messages when appropriate.
- Prefer follow-up commits on a branch already under review. Agree on history rewriting with collaborators first; never force-push `main` or rewrite someone else's work.

## Verification

Before requesting review or pushing an update, run the same check-only commands as CI:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
```

If fixes are needed, `make ruff` applies lint fixes and formatting; inspect its diff and rerun the check-only commands. See the README's [command caveats](README.md#development-commands) before using other convenience targets.

Choose behavioral verification based on the change:

| Change | Expected verification |
| --- | --- |
| Test or suite-specific implementation | Run focused tests, then the affected API/UI suite |
| Shared configuration, imports, dependencies, or fixtures | Check collection and run both suites |
| Allure hooks or reporting | Check generated report content; verify failure attachments when relevant |
| Workflow changes | Verify affected dispatch inputs, success/failure paths, artifacts, and publishing as applicable |
| Documentation only | Check paths, links, and documented commands; live test execution is optional |

The automatic `ruff + ty` check does **not** run tests. Record the exact commands and outcomes in the PR body, with workflow/run links when relevant. If tests could not run, state which ones and why; do not describe collection-only or static checks as passing tests.

Tests depend on a live external demo. Keep evidence of environment-related failures and report them instead of weakening checks to make the suite pass. The README documents [environment setup](README.md#environment-configuration) and [artifact-preserving collection](README.md#running-tests).

### Deliberate failure experiments

When a task requires proving a red/green path, keep the experiment on the PR branch, clearly label the break and restoration commits, and restore the correct test/code before merge. The final diff must not contain the deliberate mistake. Put links to the failing and restored runs, plus any merge-blocking or artifact evidence, in the PR body.

If verification can only happen after a workflow first reaches `main`, document the remaining steps and who will perform them before merge. Never use a broken test on `main` as the experiment.

## Pull requests

Use the same `type(scope): summary` style for PR titles; scope remains optional. Use the [PR template](.github/pull_request_template.md) as a starting point, scaling the detail to the change.

The PR body should answer:

- **What and why?** Summarize the behavior or maintenance improvement. Link the issue; use `Closes #<number>` only if the PR completes it, otherwise `Refs #<number>`.
- **What decisions matter?** Explain non-obvious choices, deviations from the issue, limitations, and intentionally deferred work. A small follow-up can reference the earlier review rather than repeat its entire history.
- **How was it verified?** Give commands and outcomes, relevant browser/suite selections, and run/report links or sanitized screenshots. Explicitly list anything not verified.

Keep this information in the **PR body**. Reviewers should not need to reconstruct the evidence from a comment thread. Explain a deliberate behavior change rather than presenting it as mechanical cleanup.

Before merging:

- Meet the issue's acceptance criteria or agree on the documented exceptions.
- Address review feedback and obtain reviewer approval; explain any suggestion you did not adopt.
- Keep the branch up to date with `main` and the required `ruff + ty` check green. The current `main` rules require the check and prohibit force pushes; do not bypass them.
- Restore all deliberate test failures and review the final diff for sensitive data and generated artifacts.

Branch naming, commit formatting, PR descriptions, and review expectations are documented project conventions; not all are enforced by GitHub settings or CI. Do not change those settings as part of an unrelated contribution.
