.PHONY: help install test test-smoke test-regression test-pet test-store test-user lint format clean report ci

# Переменные
PYTHON = python3
PYTEST = pytest
ALLURE = allure

# Цвета для вывода
GREEN = \033[0;32m
RED = \033[0;31m
NC = \033[0m # No Color

help:
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo "  make install        - Установка зависимостей"
	@echo "  make test           - Запуск всех тестов"
	@echo "  make test-smoke     - Запуск smoke тестов"
	@echo "  make test-regression- Запуск регрессионных тестов"
	@echo "  make test-pet       - Запуск тестов Pet API"
	@echo "  make test-store     - Запуск тестов Store API"
	@echo "  make test-user      - Запуск тестов User API"
	@echo "  make lint           - Проверка стиля кода"
	@echo "  make format         - Форматирование кода"
	@echo "  make clean          - Очистка временных файлов"
	@echo "  make report         - Генерация Allure отчёта"
	@echo "  make ci             - Запуск как в CI (линтер + тесты)"

install:
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "$(GREEN)Готово!$(NC)"

test:
	@echo "$(GREEN)Запуск всех тестов...$(NC)"
	$(PYTEST) tests/ -v

test-smoke:
	@echo "$(GREEN)Запуск smoke тестов...$(NC)"
	$(PYTEST) tests/ -m smoke -v

test-regression:
	@echo "$(GREEN)Запуск регрессионных тестов...$(NC)"
	$(PYTEST) tests/ -m "not slow" -v

test-pet:
	@echo "$(GREEN)Запуск тестов Pet API...$(NC)"
	$(PYTEST) tests/test_pet.py -v

test-store:
	@echo "$(GREEN)Запуск тестов Store API...$(NC)"
	$(PYTEST) tests/test_store.py -v

test-user:
	@echo "$(GREEN)Запуск тестов User API...$(NC)"
	$(PYTEST) tests/test_user.py -v

test-negative:
	@echo "$(GREEN)Запуск негативных тестов...$(NC)"
	$(PYTEST) tests/ -m negative -v

lint:
	@echo "$(GREEN)Проверка стиля кода...$(NC)"
	@# Установка линтеров, если их нет
	@pip install flake8 black mypy 2>/dev/null || true
	@echo "$(GREEN)Flake8:$(NC)"
	flake8 api/ tests/ utils/ models/ --max-line-length=120 --ignore=E203,W503
	@echo "$(GREEN)Black (проверка):$(NC)"
	black --check api/ tests/ utils/ models/ --line-length 100

format:
	@echo "$(GREEN)Форматирование кода...$(NC)"
	@pip install black 2>/dev/null || true
	black api/ tests/ utils/ models/ --line-length 100
	@echo "$(GREEN)Готово!$(NC)"

clean:
	@echo "$(GREEN)Очистка временных файлов...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf reports/ allure-results/ allure-report/ htmlcov/ .tox/ 2>/dev/null || true
	@echo "$(GREEN)Готово!$(NC)"

report:
	@echo "$(GREEN)Генерация Allure отчёта...$(NC)"
	@mkdir -p reports/allure-results
	$(PYTEST) tests/ --alluredir=reports/allure-results
	@if command -v allure >/dev/null 2>&1; then \
		allure serve reports/allure-results; \
	else \
		echo "$(RED)Allure не установлен. Установите: brew install allure (macOS) или скачайте с https://allurereport.org/$(NC)"; \
	fi

ci: lint test
	@echo "$(GREEN)CI проверка пройдена!$(NC)"

quick: test-smoke
	@echo "$(GREEN)Быстрая проверка завершена!$(NC)"