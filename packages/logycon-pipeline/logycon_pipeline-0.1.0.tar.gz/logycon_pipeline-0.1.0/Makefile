.PHONY: clean install test build publish lint format

# Python interpreter
PYTHON = python3
VENV = venv
VENV_BIN = $(VENV)/bin
VENV_ACTIVATE = $(VENV_BIN)/activate

# Package name
PACKAGE = logycon-pipeline

# Development
venv:
	$(PYTHON) -m venv $(VENV)
	. $(VENV_ACTIVATE) && pip install --upgrade pip
	. $(VENV_ACTIVATE) && pip install -e ".[dev]"

install: venv
	. $(VENV_ACTIVATE) && pip install -e .

# Testing
test: venv
	. $(VENV_ACTIVATE) && pytest tests/ -v

# Building
build: venv
	. $(VENV_ACTIVATE) && python -m build

# Publishing
publish: build
	. $(VENV_ACTIVATE) && python -m twine upload dist/*

# Linting and formatting
lint: venv
	. $(VENV_ACTIVATE) && flake8 src/ tests/
	. $(VENV_ACTIVATE) && mypy src/ tests/

format: venv
	. $(VENV_ACTIVATE) && black src/ tests/
	. $(VENV_ACTIVATE) && isort src/ tests/

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +

# Development dependencies
dev-deps: venv
	. $(VENV_ACTIVATE) && pip install -e ".[dev]"

# Help
help:
	@echo "Available commands:"
	@echo "  make venv        - Create virtual environment"
	@echo "  make install     - Install package in development mode"
	@echo "  make test        - Run tests"
	@echo "  make build       - Build package"
	@echo "  make publish     - Publish package to PyPI"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make dev-deps    - Install development dependencies" 