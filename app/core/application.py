from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.api.example.views import router as example_router
from app.api.user.views import router as user_router

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


def get_app():
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

    @api.on_event("startup")
    async def startup_event():
        await initialize()

    return api
