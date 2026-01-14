.PHONY: help setup dev validate test clean generate

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment
	@bash scripts/dev-setup.sh

dev: ## Start development environment
	@docker-compose up dev

validate: ## Validate all skills
	@docker-compose run --rm validator

test: ## Run tests
	@docker-compose run --rm dev pytest tests/

clean: ## Clean generated files
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".pytest_cache" -delete
	@rm -rf .coverage htmlcov/
	@echo "✓ Cleaned"

generate: ## Generate all skills
	@python tools/generate-all-skills.py

generate-batch: ## Generate specific batch (usage: make generate-batch BATCH=01)
	@python tools/generate-all-skills.py --batch $(BATCH)

generate-priority: ## Generate high priority skills
	@python tools/generate-all-skills.py --priority high

retry: ## Retry failed skills
	@python tools/generate-all-skills.py --retry

docs: ## Start documentation server
	@docker-compose up docs

search: ## Start search service
	@docker-compose up search

lint: ## Run linters
	@docker-compose run --rm dev black --check .
	@docker-compose run --rm dev ruff check .
	@docker-compose run --rm dev mypy .

format: ## Format code
	@docker-compose run --rm dev black .
	@docker-compose run --rm dev ruff check --fix .

install: ## Install dependencies
	@pip install -r requirements-dev.txt
	@npm install

shell: ## Open development shell
	@docker-compose run --rm dev /bin/bash