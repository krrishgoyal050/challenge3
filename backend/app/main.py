import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import sentry_sdk

from app.api.router import api_router
from app.core.config import get_settings


settings = get_settings()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.environment)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.getLogger("carbon").info("service_started", extra={"environment": settings.environment})
    yield
    logging.getLogger("carbon").info("service_stopped")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-powered carbon footprint tracking, planning, recommendations, and gamification.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(settings.frontend_origin)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)
Instrumentator().instrument(app).expose(app)


@app.get("/healthz", tags=["health"])
async def healthz() -> dict[str, str]:
    return {"status": "ok"}
