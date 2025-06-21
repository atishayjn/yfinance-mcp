# builder stage
FROM ghcr.io/astral-sh/uv:0.5-python3.11-bookworm-slim AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install deps
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Install project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000
RUN useradd -m appuser
USER appuser

CMD ["uv", "run", "server.py"]