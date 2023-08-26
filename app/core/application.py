import redis
import sentry_sdk

# from redis_om import get_redis_connection
from aredis_om import get_redis_connection
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.api.example.views import router as example_router
from app.api.user.schemas import User2
from app.api.user.views import router as user_router
from app.core.config import settings

# This Redis instance is tuned for durability.
REDIS_DATA_URL = "redis://localhost:6379"

# This Redis instance is tuned for cache performance.
REDIS_CACHE_URL = "redis://localhost:6381"

# from

home_router = APIRouter(tags=["System"])


class StatusCheck(BaseModel):
    status: bool
    detail: str


@home_router.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@home_router.get("/status")
async def health_status_check() -> StatusCheck:
    return {"status": True, "detail": "API is up and running "}


async def initialize():
    ...


async def initialize_redis():
    # r = redis.asyncio.from_url(REDIS_CACHE_URL, encoding="utf8",
    #                       decode_responses=True)
    # FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")

    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    User2.Meta.database = get_redis_connection(
        url=REDIS_DATA_URL, decode_responses=True
    )


def get_app():
    if not settings.debug:
        sentry_sdk.init(
            dsn=settings.sentry_logger_url,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=1.0,
        )
    api = FastAPI(
        title="Talknaw Authentication Routes",
        description=(
            "This routes here authenticate requests "
            "for all other services of the Talknaw Project\t"
            "As well as perform all necessary authentation services"
        ),
        version="0.0.1",
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

    @api.on_event("startup")
    async def startup_event():
        await initialize()
        print("connecting........................")
        # await initialize_redis()
        print("connected")

    return api
