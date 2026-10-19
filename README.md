## Allure Report

### Run tests and generate the report

Run tests and generate a fresh Allure report:

```bash
uv run allure run -- uv run pytest
```

Open the report in the browser automatically:

```bash
uv run allure run --open -- uv run pytest
```

### Generate and open Allure report after run

```bash
allure generate allure-results --clean && allure open allure-report
```

### View the report

Serve the results directly without generating a report directory:

```bash
uv run allure serve allure-results
```

Generate the HTML report manually:

```bash
uv run allure generate allure-results -o allure-report
```

### Run specific tests by Allure metadata

Run only critical tests:

```bash
uv run pytest --allure-severities=critical
```

Run tests by story:

```bash
uv run pytest --allure-stories="Invalid Credentials Rejection"
```

Run tests by requirement ID:

```bash
uv run pytest --allure-ids=FR_AUTH_003
```

Allure artifacts (`allure-results/`, `allure-report/` and `test-results/`) are excluded from version control.