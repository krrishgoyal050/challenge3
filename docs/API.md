# REST API Documentation

The backend exposes OpenAPI at `/docs` and `/openapi.json`.

## Auth

- `POST /api/v1/auth/register`: create user and return JWT access and refresh tokens.
- `POST /api/v1/auth/login`: authenticate with email/password.
- `POST /api/v1/auth/refresh`: rotate access token from refresh token.

## Activities

- `POST /api/v1/activities`: calculate and store emissions using O(1) hash-map factor lookup.
- `GET /api/v1/activities`: list user activity logs.
- `GET /api/v1/activities/dashboard`: return total emissions, score, category breakdown, sliding-window spikes, and regression forecast.

## Recommendations and AI

- `GET /api/v1/recommendations`: returns heap-ranked recommendations by impact and effort.
- `GET /api/v1/recommendations/plan`: returns DP-optimized plan, greedy quick wins, and graph traversal results.
- `POST /api/v1/recommendations/assistant`: Gemini-powered coaching with deterministic fallback.

## Goals and Gamification

- `POST /api/v1/goals`: create reduction goal.
- `GET /api/v1/goals`: list goals with forecast completion.
- `GET /api/v1/gamification/profile`: levels, badges, challenges, and leaderboard.
