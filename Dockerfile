# ── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files and install deps into an isolated venv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy the venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY . .

# Make the venv the active Python
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# The ChromaDB vector store (data/chroma_db/) is bundled in the image.
# It is excluded from .gitignore but included here via COPY . .
# No ingest step needed at runtime.

EXPOSE 7860

CMD ["chainlit", "run", "ui/ui.py", "--host", "0.0.0.0", "--port", "7860"]
