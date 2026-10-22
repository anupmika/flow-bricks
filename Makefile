TOP_DIR := $(shell git rev-parse --show-toplevel)
SRC_DIR := "$(TOP_DIR)/src"
APP_PY  := "$(SRC_DIR)/app.py"

all: clean sync run

sync:
	@uv sync --no-cache

debug: sync
	@uv run streamlit run "$(APP_PY)" --server.runOnSave true

run: sync
	@uv run streamlit run "$(APP_PY)"

test: sync
	@echo "No tests available currently."

clean:
	@uv clean
	@rm -rf __pycache__ .pytest_cache .mypy_cache .venv

.PHONY: all sync debug run test clean
