from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.system.schema import StatusCheck

router = APIRouter(tags=["System"])


@router.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@router.get("/status")
async def health_status_check() -> StatusCheck:
    return {"status": True, "detail": "API is up and running "}
