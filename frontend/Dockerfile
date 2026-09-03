# Frontend multi-stage build for Next.js
# Builder
FROM node:20 AS builder
WORKDIR /app

ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

# Copy frontend sources
COPY frontend/package*.json ./
COPY frontend/package-lock.json frontend/yarn.lock ./ || true
COPY frontend/ .

# Install and build
RUN npm ci --production=false --silent
RUN npm run build --if-present

# Production image
FROM node:20-alpine
WORKDIR /app

ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

# Copy built assets and production node_modules
COPY --from=builder /app/ .

EXPOSE ${PORT:-3000}

# Start server on $PORT (Next.js start expects build to exist)
CMD ["sh", "-c", "npm start -- -p ${PORT:-3000}"]
