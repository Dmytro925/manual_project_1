# QA Demo test automation

UI and API tests for the [QA Demo e-commerce store](https://qademo.com/), built with Python 3.14, pytest, Playwright, requests, and Allure Report. Dependencies are managed with uv.

> **Status: work in progress.** This is an early-stage test framework with partial, growing coverage. Page objects, API clients, fixtures, tests, and workflows may change as the project develops. These docs describe the current state, not a finished feature set or stable interfaces. Follow the [documentation maintenance rules](CONTRIBUTING.md#documentation-maintenance) as the project evolves.

This is a test repository, not the store's application code. Tests run against an external environment; there is no local server to start. Current coverage includes login, rejected credentials, logout, session persistence, protected-route redirects, and the products API.

[Published reports](https://dmytro925.github.io/manual_project_1/) · [Contributing](CONTRIBUTING.md) · [Coding standards](CODING_STANDARDS.md)

## Quick start

Prerequisites: [uv](https://docs.astral.sh/uv/getting-started/installation/), Python 3.14 (see `.python-version`), and Git. Make is optional; the underlying commands use `uv run`.

```bash
git clone https://github.com/Dmytro925/manual_project_1.git
cd manual_project_1
uv sync --locked
cp .env.example .env
uv run playwright install chromium
```

Fill in `.env` as described below **before running pytest**. The example contains placeholders, not working configuration. Then run:

```bash
uv run pytest
```

API-only runs do not need Playwright browser binaries. On Linux, browser system libraries may also be needed; the CI workflow installs them with `uv run playwright install --with-deps chromium`.

## Environment configuration

Use the demo environment's standard, locked, and admin test accounts. Consult the store's login-page test-credentials helper or ask a maintainer for the appropriate values. Keep actual values in the gitignored `.env` or exported environment variables, never in tracked files. Use demo accounts, not personal or production credentials.

| Variable | Required | Purpose |
| --- | --- | --- |
| `BASE_URL` | Yes | Application origin used for relative browser URLs |
| `API_BASE_URL` | No | API origin; an empty or unset value falls back to `BASE_URL` |
| `STANDARD_USER_USERNAME` | Yes | Standard demo user's username |
| `STANDARD_USER_PASSWORD` | Yes | Standard demo user's password |
| `LOCKED_USER_USERNAME` | Yes | Locked demo user's username |
| `LOCKED_USER_PASSWORD` | Yes | Locked demo user's password |
| `ADMIN_USER_USERNAME` | Yes | Admin demo user's username |
| `ADMIN_USER_PASSWORD_TEMPLATE` | Yes | Admin password template containing `{date}` |

`config/__init__.py` loads the root `.env` without interpolating `$` expressions. Exported variables take precedence, so CI does not need an `.env` file. Missing required variables raise an error naming the variable; some credentials are read during test collection.

The admin template's `{date}` is replaced with the current date in `DDMMYYYY` format using the machine's local time. GitHub-hosted runners use UTC. Keep the template rather than saving today's generated password; check the date/time zone if only admin login fails around midnight.

## Running tests

Run commands from the repository root:

| Command | Purpose |
| --- | --- |
| `make tests` | Run all tests |
| `make api-tests` | Run API tests |
| `make ui-tests` | Run UI tests with Chromium, the default browser |
| `make tests TEST=tests/ui_tests/test_login_page.py::test_locked_user_cannot_login` | Run one test |
| `uv run pytest tests/api_tests/` | Run a suite without Make |

To use another browser, install it and select it explicitly:

```bash
uv run playwright install firefox
uv run pytest tests/ui_tests/ --browser firefox
```

`webkit` is also supported. To check discovery without running tests or clearing previous Allure results:

```bash
uv run pytest --collect-only -q -o addopts=''
```

Collection still needs environment configuration. Normal test runs clear `allure-results/` because `--clean-alluredir` is configured in `pyproject.toml`; save evidence you need before another run.

## Development commands

| Command | Purpose |
| --- | --- |
| `make help` | List Make targets |
| `make sync` | Sync dependencies with uv |
| `make ruff` | Auto-fix lint findings and format Python files |
| `make ty` | Check types |
| `make codegen` | Open Playwright code generation against the fixed demo-store URL |
| `make clean` | Delete local Allure results and the generated report |

`make codegen` currently uses a hardcoded URL in `Makefile`, not `BASE_URL`. The tests themselves use environment configuration.

For non-mutating checks matching CI, use [Contributing → Verification](CONTRIBUTING.md#verification). **`make check` is not check-only:** it invokes the auto-fixing and formatting `ruff` target before type checking.

## Allure reports

Every normal pytest run writes results to `allure-results/`. The root hook adds environment information; failed UI tests save screenshots under `test-results/` and attach them to Allure automatically. These directories and `allure-report/` are gitignored.

The Python integration is installed by uv. The **Allure 3 CLI** is separate and needs Node.js/npm:

```bash
npm install -g allure
allure --version
```

Generate and open a report from existing results, without rerunning tests:

```bash
allure generate allure-results -o allure-report
allure open allure-report
```

Stop the report server with `Ctrl+C`. Use a fresh output directory when you need an isolated report for one run.

**Known helper limitation:** `make allure` currently passes `--clean`, which Allure 3 does not support. Use the commands above until the Make target is updated. See the official [installation](https://allurereport.org/docs/v3/install/), [generation](https://allurereport.org/docs/v3/generate-report/), and [viewing](https://allurereport.org/docs/v3/view-report/) guides.

**Public-report warning:** logs, report parameters, and screenshots may contain authentication data. The API client currently logs full response bodies, including login responses; readable pytest parameter IDs do not remove values from Allure data. Review and sanitize artifacts before publishing or sharing them. See [output safety](CODING_STANDARDS.md#configuration-and-output-safety).

## GitHub Actions

### Automatic checks

[CI](.github/workflows/ci.yml) runs on every PR and push to `main`. Its `ruff + ty` job performs lint, format, and type checks. **It does not execute tests.**

### On-demand tests and published reports

[Tests](.github/workflows/tests.yml) runs only through `workflow_dispatch`:

1. Configure repository Actions secrets with the environment-variable names listed above. `API_BASE_URL` remains optional. `GITHUB_TOKEN` is supplied automatically by GitHub.
2. Open **Actions → Tests → Run workflow** and select the branch, suite (`all`, `api`, or `ui`), and browser (`chromium`, `firefox`, or `webkit`).
3. Inspect the test jobs and their `allure-results-api` / `allure-results-ui` artifacts. Results are uploaded even when tests fail, if result files were produced.
4. Open the [published reports](https://dmytro925.github.io/manual_project_1/). Publishing can succeed for a failing test run; the workflow still reports the test failure.

API and UI reports are built separately and published together to the generated `gh-pages` branch. A maintainer setting up a fork must enable Pages with **Deploy from a branch → `gh-pages` → `/(root)`** after the first publish.

The site represents the latest publish, not an archive: an API-only publish replaces the previous site with only the API report. Cross-run Allure history is not preserved. Pages/browser caching can show an older report for about ten minutes; compare the run ID in the index, check `gh-pages`, and refresh or wait rather than dispatching another run just to refresh the site.

## Repository layout

```text
config/                 Environment loading and credential getters
src/api/                HTTP clients and authenticated user sessions
src/pages/              Page objects and shared UI components
tests/api_tests/        API tests and fixtures
tests/ui_tests/         UI tests, fixtures, and screenshot attachment hook
conftest.py             Shared pytest configuration and Allure environment hook
.github/workflows/      Static checks and manual test/report workflows
```

For contribution workflow, commit messages, and PR expectations, read [CONTRIBUTING.md](CONTRIBUTING.md). Code and test conventions live in [CODING_STANDARDS.md](CODING_STANDARDS.md); [AGENTS.md](AGENTS.md) directs coding agents to the relevant guidance.
