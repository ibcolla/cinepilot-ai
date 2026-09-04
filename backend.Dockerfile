FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Copy ALL source code and config files first
COPY . .

# 2. Upgrade core build tools
RUN python -m pip install --upgrade pip setuptools wheel

# 3. Install the package and its dependencies
RUN python -m pip install --no-cache-dir .

# 4. Start the server
CMD exec uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}