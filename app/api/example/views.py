from app.api.example.schemas import ExampleCreateSchema, ExampleSchema
from app.api.example.services import ExampleService
from fastapi import APIRouter

from app.database.db import AnSession
from app.database.models.example import Example

router = APIRouter(tags=["Example-Routes"], prefix="/example")



@router.get("/old", response_model=list[ExampleSchema])
async def get_examples(session: AnSession,) -> list[Example]:
    example_service = ExampleService(session=session)
    return await example_service.get_all_examples()


@router.post("/new", response_model=ExampleSchema)
async def create_example(
    data: ExampleCreateSchema,
    session: AnSession,
) -> Example:
    example_service = ExampleService(session=session)
    example = await example_service.create_example(data)
    return example
