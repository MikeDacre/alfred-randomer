.PHONY: help install build release release-patch release-minor release-major test format clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Version bumping:"
	@echo "  \033[36mmake release-patch\033[0m     Bump patch version (1.0.0 -> 1.0.1)"
	@echo "  \033[36mmake release-minor\033[0m     Bump minor version (1.0.0 -> 1.1.0)"
	@echo "  \033[36mmake release-major\033[0m     Bump major version (1.0.0 -> 2.0.0)"
	@echo ""
	@echo "For more options run: ./scripts/release.sh --help"

install: ## Install dependencies with Poetry
	poetry install

build: ## Build the Alfred workflow
	./scripts/build.sh

release: ## Create release with current version
	./scripts/release.sh

release-patch: ## Bump patch version and release
	./scripts/release.sh patch

release-minor: ## Bump minor version and release
	./scripts/release.sh minor

release-major: ## Bump major version and release
	./scripts/release.sh major

test: ## Run tests
	PYTHONPATH=src poetry run python3 -m unittest discover -s tests

format: ## Format code with Black
	poetry run black src/ tests/

clean: ## Clean build artifacts
	rm -rf dist/ releases/*.alfredworkflow
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
