TOP_DIR := `git rev-parse --show-toplevel`
SRC_DIR := TOP_DIR / "src"

[private]
default:
    @just --list --justfile {{justfile()}}

# Run the setup development environment: clean, sync
all: clean sync

# Install or update project dependencies with `uv`
sync:
    @uv sync --no-cache

# Run the test target (no tests are currently configured)
test: sync
    @echo "No tests available currently."

# Remove the local environment and generated Python caches
clean:
    @uv clean
    @rm -rf __pycache__ .pytest_cache .mypy_cache .venv
