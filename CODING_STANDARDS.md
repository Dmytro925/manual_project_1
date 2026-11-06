# Coding standards

These conventions apply to new and changed code. Keep unrelated cleanup out of a focused task. Tool configuration in [pyproject.toml](pyproject.toml) is authoritative for automated checks; the rules below also capture decisions from issue discussions and code reviews.

These are working conventions for a growing codebase, not a frozen architecture. When a task deliberately changes a convention, explain the rationale and update this guidance as part of the same change, following [documentation maintenance](CONTRIBUTING.md#documentation-maintenance).

## Python style and typing

- Use English for identifiers, comments, docstrings, and Allure text. End text files with a newline.
- Let Ruff format code. Fix lint/type errors in code rather than weakening project-wide checks to accommodate a change. Type checking uses **ty**.
- Use modern annotations such as `str | None` and `dict[str, str]`, and concrete types such as `Page`, `Locator`, `Response`, and project classes.
- Annotate function and method parameters and returns, including fixtures and pytest hooks. For test functions, annotate parameters and omit the return annotation, following the existing convention. `test_*.py` exempts `ANN201`, not all annotation rules.
- Let the checker infer local variables and instance attributes when their types are clear. Use `Any` only at genuinely dynamic boundaries, such as forwarded HTTP keyword arguments; keep suppressions narrow and justified.
- Library code and fixtures use concise Google-style docstrings with a summary ending in a period. Add `Args:` / `Returns:` sections only when useful. Module/package and `__init__` docstrings are not required by the current Ruff configuration.
- Test docstrings become Allure descriptions. Preserve their meaning during refactors, even though missing-docstring checks are relaxed for `test_*.py`.

## Imports and package interfaces

Tests and their fixtures consume the public package facades:

```python
from src.api import AuthClient, ProductsClient
from src.pages import CatalogPage, LoginPage
```

Inside those packages, import concrete sibling modules instead:

```python
from src.api.base_client import ApiClient
from src.pages.base_page import BasePage
```

Importing a package's own facade from its implementation modules can introduce circular, order-dependent imports. Export intended public classes through the package's `__init__.py` and `__all__`; use explicit imports rather than wildcard imports.

## Page objects and UI checks

- Use the synchronous Playwright API. `BasePage` wraps a `Page`; it does not subclass Playwright's `Page`. Shared navbar behavior belongs in `Navbar`.
- Keep reusable locators and interactions in page objects/components; keep scenario assertions in tests.
- Prefer `get_by_test_id(...)` when the application exposes an appropriate test ID. Otherwise use a specific role/label locator. Verify that the locator exists and uniquely identifies the intended element; avoid duplicate aliases for the same control.
- Navigate and assert URLs with relative paths, such as `page.goto("/login")` and `expect(page).to_have_url("/catalog")`. The root pytest configuration supplies the environment-specific base URL.
- Use Playwright's retrying `expect(...)` assertions and observable readiness conditions, not fixed sleeps. Keep page objects reusable: pass a product name to an interaction instead of binding the constructor to one product.

## API clients and fixtures

- Put reusable HTTP behavior in `ApiClient` and endpoint-specific behavior in the appropriate client. API tests use requests-based clients independently of browser fixtures.
- API responses are already logged through the base client's response hook. Use that logging rather than adding per-test prints or duplicate response dumps.
- The fixture that creates an HTTP session owns its cleanup: yield the client and close it during teardown. A `UserClient` returned by `AuthClient.login()` shares the authentication client's session, so its dependent fixture should not close that session again.
- Fixtures prepare reusable starting states, such as an authenticated catalog or a cart containing a product. Keep scenario-specific actions, such as logout, and their assertions visible in the test. Reuse fixture dependencies instead of repeating setup sequences.
- Keep tests independent of execution order and other tests' state. Use the narrowest practical fixture scope, with cleanup for resources the fixture owns.

## Test layout and reporting

- Use one file per UI page or API module, directly under the corresponding suite: `test_login_page.py`, `test_auth.py`, `test_products.py`. Names are lowercase snake_case; requirement IDs and numeric ordering prefixes belong outside filenames.
- Write plain test functions named for the subject and expected behavior: `test_<subject>_<expected_behavior>`. Use Allure's hierarchy instead of test classes to group scenarios.
- New tests include `allure.id`, `epic`, `feature`, `story`, `severity`, and a readable `title`. Preserve this metadata when moving tests.
- Requirement IDs use the existing hyphenated format, such as `FR-AUTH-004`. Match the issue/spec's mapping rather than inventing IDs or using GitHub issue numbers. API and UI tests currently share IDs for the same requirement; unrelated scenarios must not borrow those IDs. Confirm an unclear mapping with a maintainer.
- Use `with allure.step("..."):` around logical test sections, not `@allure.step` decorators. Keep steps meaningful rather than wrapping every statement.
- Use descriptive docstrings for report descriptions. Parameter substitution belongs in `@allure.title`, not docstrings; only substitute non-sensitive values.
- Parameterize input variations with readable, non-sensitive `ids=` labels. Parameterized variants share their test's requirement ID.
- For API checks, verify the status before asserting the response body's contract. Derive expectations from requirements, not merely from what the current demo happens to return. Investigate external-app failures rather than relaxing assertions to obtain a green run.

## Configuration and output safety

- Read environment-specific URLs and credentials through `config/environments.py`. Keep `.env.example` as a placeholder-only inventory; when adding a variable, update its getter, setup documentation, and workflow environment mapping as applicable.
- Keep credentials, tokens, and generated artifacts out of commits, PR descriptions, step names, and attachments shared for review.
- For new credential scenarios, parameterize scenario labels and resolve credentials inside the fixture/test rather than parameterizing raw passwords. Explicit pytest `ids=` only makes node IDs readable; Allure still records parameter values. Masked/hidden display modes are not a substitute for removing secrets from stored data.
- The response hook logs bodies only at `DEBUG`; default `INFO` runs log the method, URL, and status. Debug runs and captured parameters can still contain credentials, so treat logs and report artifacts as potentially sensitive; inspect and sanitize the actual stored files before public publication. GitHub Pages reports are public.

## Workflow changes

- Preserve the separation between automatic static checks and manually dispatched live tests. Keep the `ruff + ty` check name aligned with the repository's required-check rules.
- Keep lint, format checking, and type checking as separate, non-mutating CI steps. Local verification commands are in [CONTRIBUTING.md](CONTRIBUTING.md#verification).
- Preserve failure evidence: upload available results even when tests fail, allow report generation from whichever suite produced results, and keep the test failure visible in the workflow conclusion.
- Grant write permissions only to jobs that need them, currently the report-publishing job. Verify action references against real upstream tags instead of guessing a floating major version.

## Background decisions

For rationale, see issues [#8](https://github.com/Dmytro925/manual_project_1/issues/8) (facades), [#9](https://github.com/Dmytro925/manual_project_1/issues/9) / [#10](https://github.com/Dmytro925/manual_project_1/issues/10) (typing/docstrings), [#17](https://github.com/Dmytro925/manual_project_1/issues/17) (test layout), [#23](https://github.com/Dmytro925/manual_project_1/issues/23) (review fixes), and [#24](https://github.com/Dmytro925/manual_project_1/issues/24), [#27](https://github.com/Dmytro925/manual_project_1/issues/27), [#28](https://github.com/Dmytro925/manual_project_1/issues/28) (CI and reports). This document consolidates the current conventions; historical issues may contain superseded instructions.
