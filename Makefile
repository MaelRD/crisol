.PHONY: install dev test lint format typecheck check

install:  ## Create .venv and install all dependencies (incl. dev)
	uv sync

dev:  ## Run the API with auto-reload
	uv run uvicorn crisol.main:create_app --factory --reload --host 127.0.0.1 --port 8000

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run mypy src

check: lint typecheck test  ## Everything CI would run
