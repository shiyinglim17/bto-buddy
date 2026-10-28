# syntax=docker/dockerfile:1
# Two stages: uv installs the locked dependencies; the runtime image carries only the
# virtualenv and the app source (no uv, no build tooling, no private data).

FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /app

# Dependencies first, so this layer is cached until uv.lock changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Then the project itself, installed as a regular (non-editable) package.
COPY README.md ./
COPY src/ src/
RUN uv sync --frozen --no-dev --no-editable


FROM python:3.12-slim AS runtime
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true
RUN useradd --create-home --uid 1000 app
WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app src/bto_buddy/app.py ./app.py
COPY --chown=app:app .streamlit/config.toml ./.streamlit/config.toml
USER app

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=4)"

# Configuration (LLM settings) is read from environment variables: docker run --env-file .env
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
