FROM mcr.microsoft.com/devcontainers/python:3.12

ENV ANONYMIZED_TELEMETRY=false \
  DEBIAN_FRONTEND=noninteractive \
  PIP_NO_CACHE_DIR=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
  UV_LINK_MODE=copy

USER vscode

RUN pip install --no-cache-dir \
  rust-just \
  uv
