from contextlib import asynccontextmanager

import sentry_sdk
from aredis_om import get_redis_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.system.views import router as home_router
from app.api.user.schemas import User2
from app.api.user.views import router as user_router
from app.core.config import settings

# This Redis instance is tuned for durability.
REDIS_DATA_URL = "redis://localhost:6379"

# This Redis instance is tuned for cache performance.
REDIS_CACHE_URL = "redis://localhost:6381"

# from


@asynccontextmanager
async def lifespan(api: FastAPI):
    print("Starting Server and connecting all dependencies")
    User2.Meta.database = get_redis_connection(
        url=REDIS_DATA_URL, decode_responses=True
    )

    if not settings.debug:
        sentry_sdk.init(
            dsn=settings.sentry_logger_url,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=1.0,
        )

    yield

    print("Closing all resources and shutting down the application")


def get_app():
    api = FastAPI(
        title="Talknaw Authentication Routes",
        description=(
            "This routes here authenticate requests "
            "for all other services of the Talknaw Project\t"
            "As well as perform all necessary authentation services"
        ),
        version="0.0.1",
        lifespan=lifespan,
    )

    # api.include_router(example_router)
    api.include_router(user_router)
    api.include_router(home_router)

    api.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return api
