FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only packaging metadata first to leverage Docker layer cache
COPY pyproject.toml .
COPY poetry.lock* . || true

# Upgrade pip and install the package
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install --no-cache-dir .

# Copy application source
COPY . /app

EXPOSE 8000

# Run using environment PORT (default 8000)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
