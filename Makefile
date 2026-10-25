.DEFAULT_GOAL := help

# ---------- Налаштування ----------

PYTHON_RUN := uv run
PYTEST := $(PYTHON_RUN) pytest

ALLURE_RESULTS := allure-results
ALLURE_REPORT := allure-report

TEST ?= tests/

# ---------- Службові команди ----------

.PHONY: help sync
.PHONY: test test-auth test-api
.PHONY: ruff ty check
.PHONY: allure clean

help: ## Показати доступні команди
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*##"} {printf "  %-18s %s\n", $$1, $$2}'

sync: ## Синхронізувати залежності з uv.lock
	uv sync

# ---------- Pytest ----------

tests: ## Запустити тести або шлях із TEST
	$(PYTEST) $(TEST)

api-tests: ## Запустити всі API-тести
	$(PYTEST) tests/api_tests/

ui-tests: ## Запустити всі UI-тести
	$(PYTEST) tests/ui_tests/

# ---------- Ruff ----------

ruff: ## Виправити помилки та відформатувати код
	$(PYTHON_RUN) ruff check . --fix
	$(PYTHON_RUN) ruff format .

# ---------- Ty ----------

ty: ## Перевірити типи Python через ty
	$(PYTHON_RUN) ty check

# ---------- Комплексна перевірка ----------

check: ruff ty ## Запустити Ruff і ty

# ---------- Allure Report ----------

test-allure: ## Запустити тести та відкрити Allure-звіт
	@set +e; \
	$(PYTEST) $(TEST); \
	test_status=$$?; \
	allure generate $(ALLURE_RESULTS) --clean -o $(ALLURE_REPORT); \
	report_status=$$?; \
	if [ $$report_status -eq 0 ]; then \
		allure open $(ALLURE_REPORT); \
	else \
		exit $$report_status; \
	fi; \
	exit $$test_status

# ---------- Очищення ----------

clean: ## Видалити результати тестів і Allure-звіт
	rm -rf $(ALLURE_RESULTS) $(ALLURE_REPORT)