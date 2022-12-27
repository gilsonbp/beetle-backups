.PHONY=help
help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.PHONY:clean
clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

###
# Dependencies section
###
.PHONY: _base_pip
_base_pip:
	@pip install -U pip poetry wheel

.PHONY: _base_poetry
_base_poetry:
	@poetry install

.PHONY: _base_pre-commit
_base_pre-commit:
	@pre-commit install --allow-missing-config
	@pre-commit install --hook-type pre-commit --hook-type pre-push

.PHONY: dev-dependencies
dev-dependencies: _base_pip _base_poetry _base_pre-commit ## Install development dependencies

.PHONY: dependencies
dependencies: _base_pip ## Install dependencies
	@poetry install --no-dev

.PHONY: ci-dependencies
ci-dependencies: _base_pip
	@poetry install

.PHONY: outdated
outdated: ## Show outdated packages
	@poetry show --outdated

###
# Lint section
###
_flake8:
	@flake8 --show-source src/

_black:
	@black --check src/

_isort:
	@isort --diff --check-only src/

_isort-fix:
	@isort src/

_black_fix:
	@black src/

_mypy:
	@mypy src/

.PHONY: lint
lint: _flake8 _isort _black _mypy   ## Check code lint

.PHONY: format-code
format-code: _isort-fix _black_fix ## Format code

.PHONY: run
run:  ## Run Worker
	@celery -A src worker --loglevel=INFO --pidfile=celery.pid

.PHONY: run-local
run-local:  ## Run Worker Local
	@watchmedo auto-restart --directory=./ --pattern='*.py' --recursive -- celery -A src worker --loglevel=INFO --pidfile=celery.pid

###
# Tests section
###
.PHONY: test-ci
test-ci: clean ## Run tests
	@pytest . --cov . --cov-report term-missing --cov-report xml

.PHONY: test
test: clean ## Run tests
	@pytest .

.PHONY: test-coverage
test-coverage: clean ## Run tests with coverage output
	@pytest . -vv -x --lf --cov src --cov-report term-missing --cov-report xml --cov-report html

.PHONY: test-debug
test-debug: clean ## Run tests with active pdb
	@pytest --pdb

.PHONY: test-matching
test-matching: clean ## Run tests by match ex: make test-matching k=name_of_test
	@pytest -k $(k) .

.PHONY: test-security
test-security: clean ## Run security tests with bandit and safety
	@python -m bandit -r . -x "test"
	@python -m safety check

.PHONY: shell
shell:
	@ipython

.PHONY: pre-commit-all
pre-commit-all: clean ## Run pre-commit in all files
	@pre-commit run -a

.PHONY: pre-commit
pre-commit: clean ## Run pre-commit
	@pre-commit
