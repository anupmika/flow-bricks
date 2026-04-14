#!/usr/bin/make -f

TOP_DIR := $(shell git rev-parse --show-toplevel)
SRC_DIR := "$(TOP_DIR)/src"

all: clean sync run

sync:
	@uv sync --no-cache

debug: sync
	@uv run streamlit run "$(SRC_DIR)/app.py" --server.runOnSave true

run: sync
	@uv run streamlit run "$(SRC_DIR)/app.py"

test: sync
	@echo "No tests available currently."

clean:
	@uv clean
	@rm -rf __pycache__ .pytest_cache .mypy_cache .venv