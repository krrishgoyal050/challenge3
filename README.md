# Carbon Footprint Awareness Platform

Production-style full-stack sustainability assistant with a Next.js frontend, FastAPI backend, PostgreSQL, Redis, Gemini AI integration, DSA-powered recommendations, observability, tests, and GCP deployment scaffolding.

## Architecture

- `frontend/`: Next.js, React, TypeScript, Tailwind CSS, accessible dashboard and calculator.
- `backend/`: FastAPI async APIs, SQLAlchemy models, Alembic migrations, JWT auth, RBAC, rate limiting, Prometheus metrics, Sentry hook.
- `backend/app/algorithms/`: required DSA modules: hash maps, heap, graph algorithms, dynamic programming, sliding window, and greedy optimization.
- `infra/terraform/`: Cloud Run, Cloud SQL PostgreSQL, Artifact Registry, and Secret Manager baseline.
- `.github/workflows/ci.yml`: backend, frontend, and security CI.

## Run Locally

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- OpenAPI: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`

Before production, copy `.env.example` files, set strong secrets, configure `GEMINI_API_KEY`, and restrict CORS origins.

## DSA Requirements

- Hash maps: `CarbonFactorStore` provides O(1) carbon factor lookup and preference caching.
- Priority queue: `RecommendationHeap` ranks actions by savings per effort.
- Graph algorithms: `bfs`, `dfs`, and `dijkstra` model relationships among transport, energy, food, shopping, and waste.
- Dynamic programming: `optimize_plan` solves weekly/monthly action selection with a knapsack strategy.
- Sliding window: `detect_spikes` finds unusual emission spikes.
- Greedy: `greedy_quick_wins` selects maximum impact-per-effort actions.

## Security

Implemented baseline controls include JWT access tokens, refresh tokens, RBAC dependency, Pydantic validation, parameterized SQLAlchemy queries, CORS configuration, rate limiting, secure environment examples, dependency scanning in CI, and non-leaking auth errors. Use managed secrets and HTTPS in production.

## Accessibility

The frontend uses semantic landmarks, labeled forms, visible focus states, ARIA labels for charts/progress, high contrast support, keyboard reachable controls, and responsive layouts intended for WCAG 2.1 AA.

## Testing

```bash
cd backend
poetry install --with dev
poetry run pytest

cd ../frontend
npm install
npm run test
npm run e2e
```

Backend coverage is configured to fail below 90%. Frontend coverage thresholds are set to 80% in this scaffold and can be raised as more UI branches are added.

## GCP Deployment

1. Create or select a GCP project.
2. Enable Cloud Run, Cloud SQL, Artifact Registry, Secret Manager, Cloud Build, and Cloud Monitoring APIs.
3. Apply Terraform:

```bash
cd infra/terraform
terraform init
terraform apply \
  -var="project_id=YOUR_PROJECT" \
  -var="backend_image=REGION-docker.pkg.dev/YOUR_PROJECT/carbon-platform/backend:TAG" \
  -var="frontend_image=REGION-docker.pkg.dev/YOUR_PROJECT/carbon-platform/frontend:TAG"
```

4. Use `cloudbuild.yaml` to build and deploy Cloud Run revisions.

## Production Notes

- Run Alembic migrations during release.
- Store JWT, database, Gemini, and Sentry secrets in Secret Manager.
- Use Cloud SQL private connectivity for backend-to-database traffic.
- Add Redis Memorystore for distributed caching and rate limiting.
- Configure Grafana or Cloud Monitoring dashboards over `/metrics`.
- Add Sentry DSN for exception tracing.
