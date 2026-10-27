.DEFAULT_GOAL := help

# ---------- Configuration ----------

PYTHON_RUN := uv run
PYTEST := $(PYTHON_RUN) pytest

ALLURE_RESULTS := allure-results
ALLURE_REPORT := allure-report

TEST ?= tests/

# ---------- Utility Commands ----------

.PHONY: help sync
.PHONY: tests api-tests ui-tests
.PHONY: ruff ty check
.PHONY: test-allure clean

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*##"} {printf "  %-18s %s\n", $$1, $$2}'

sync: ## Sync dependencies with uv.lock
	uv sync

# ---------- Pytest ----------

tests: ## Run all tests or a specific path using TEST
	$(PYTEST) $(TEST)

api-tests: ## Run all API tests
	$(PYTEST) tests/api_tests/

ui-tests: ## Run all UI tests
	$(PYTEST) tests/ui_tests/

# ---------- Ruff ----------

ruff: ## Fix lint issues and format code
	$(PYTHON_RUN) ruff check . --fix
	$(PYTHON_RUN) ruff format .

# ---------- Ty ----------

ty: ## Check Python types with ty
	$(PYTHON_RUN) ty check

# ---------- Code Checks ----------

check: ruff ty ## Run Ruff and ty checks

# ---------- Allure Report ----------

allure: ## Generate and open the Allure report
	allure generate $(ALLURE_RESULTS) --clean -o $(ALLURE_REPORT)
	allure open $(ALLURE_REPORT)

# ---------- Cleanup ----------

clean: ## Remove test results and the Allure report
	rm -rf $(ALLURE_RESULTS) $(ALLURE_REPORT)

# ---------- Codegen ----------

codegen: ## Run Codegen browser
	uv run playwright codegen --target python-pytest https://qademo.com/