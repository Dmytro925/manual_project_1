# AGENTS.md

Early-stage, actively evolving Python 3.14 test automation using uv, pytest, Playwright, requests, and Allure. This repository tests an external demo store; there is no local application or service to start.

## Read before work

- **Setup, test commands, environment failures, or reports:** read [README.md](README.md), including the command caveats.
- **Writing or reviewing Python, tests, or workflows:** read [CODING_STANDARDS.md](CODING_STANDARDS.md).
- **Planning any change, preparing commits, pushing, or working on a PR:** read [CONTRIBUTING.md](CONTRIBUTING.md), including documentation maintenance and verification requirements.

These files own their respective guidance. Update the relevant document when behavior or policy changes rather than copying its rules here.

## Current working map

- `src/pages/` — synchronous Playwright page objects; `BasePage` wraps `Page` and provides the shared `Navbar`.
- `src/api/` — requests-based clients; `AuthClient.login()` returns a `UserClient` sharing the authentication client's HTTP session.
- `config/environments.py` — environment access and credential getters. Importing `config` loads the optional root `.env`; exported variables also work.
- `tests/api_tests/conftest.py` and `tests/ui_tests/conftest.py` — suite-specific fixtures; root `conftest.py` sets Playwright's base URL and writes Allure environment information.
- `.github/workflows/ci.yml` — automatic static checks; `tests.yml` — manually dispatched tests and public report publishing.

## Execution

- Run project commands from the repository root with `uv run` or the documented Make targets.
- Before handing off any change, complete [documentation maintenance](CONTRIBUTING.md#documentation-maintenance) and [verification](CONTRIBUTING.md#verification). Report actual results and explicitly identify tests not run.
- Preserve existing `.env` values. If configuration is missing, ask for setup using the README rather than inventing credentials.
- Default pytest runs replace previous Allure results. Use the README's artifact-preserving collection command when only checking discovery.

## Agent permissions

Contribution instructions describe the workflow, not authorization to perform Git or GitHub actions. Commit, push, create or merge PRs, dispatch workflows, or change GitHub settings only when the user explicitly requests those actions.
