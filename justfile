TOP_DIR := `git rev-parse --show-toplevel`
SRC_DIR := TOP_DIR / "src"
APP_PY  := SRC_DIR / "app.py"

# Default recipe (runs when you just type 'just')
all: clean sync run

# Sync dependencies using uv
sync:
    @uv sync --no-cache

# Run streamlit in debug mode
debug: sync
    @uv run streamlit run {{APP_PY}} --server.runOnSave true

# Standard run
run: sync
    @uv run streamlit run {{APP_PY}}

# Placeholder for tests
test: sync
    @echo "No tests available currently."

# Clean up environment and caches
clean:
    @uv clean
    @rm -rf __pycache__ .pytest_cache .mypy_cache .venv
