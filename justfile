TOP_DIR := `git rev-parse --show-toplevel`
SRC_DIR := TOP_DIR / "src"
APP_PY := SRC_DIR / "app.py"

[private]
default:
    @just --list --justfile {{justfile()}}

# Run the full development workflow: clean, sync, and start the app
all: clean sync run

# Install or update project dependencies with `uv`
sync:
    @uv sync --no-cache

# Run Streamlit with automatic reload when source files change
debug: sync
    @uv run streamlit run {{ APP_PY }} --server.runOnSave true

# Run Streamlit in standard mode
run: sync
    @uv run streamlit run {{ APP_PY }}

# Run the test target (no tests are currently configured)
test: sync
    @echo "No tests available currently."

# Remove the local environment and generated Python caches
clean:
    @uv clean
    @rm -rf __pycache__ .pytest_cache .mypy_cache .venv
