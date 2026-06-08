# Root Dockerfile for Cloud Run "deploy from source" flows.
# It deploys the Next.js frontend from the monorepo root.
FROM node:22-alpine AS deps

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install

FROM node:22-alpine AS builder

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY frontend/ ./
RUN mkdir -p public
RUN npm run build

FROM node:22-alpine AS runner

WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["sh", "-c", "npm run start -- -p ${PORT:-3000}"]
