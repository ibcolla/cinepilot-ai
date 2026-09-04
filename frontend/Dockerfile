# Frontend multi-stage build for Next.js
# Builder
FROM node:20 AS builder
WORKDIR /app

ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

# Safely copy package files using wildcards
COPY package*.json yarn.lock* ./
COPY . .

# Force install past peer dependency conflicts
RUN npm install --legacy-peer-deps

# Explicitly install the missing CSS dependency
RUN npm install autoprefixer postcss tailwindcss --legacy-peer-deps

# Build the Next.js app (ignoring lint errors)
RUN NEXT_IGNORE_ESLINT=1 npm run build

# Production image
FROM node:20-alpine
WORKDIR /app

ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

# Copy built assets
COPY --from=builder /app/ .

EXPOSE ${PORT:-3000}

# Start server on $PORT
CMD ["sh", "-c", "npm start -- -p ${PORT:-3000}"]