from app.api.example.schemas import ExampleCreateSchema
from sqlalchemy import select

from app.database.db import AnSession
from app.database.models.example import Example


class ExampleService:
    def __init__(self, session:AnSession):
        self.session = session

    async def get_all_examples(self) -> list[Example]:
        examples = await self.session.execute(select(Example))

        return examples.scalars().fetchall()

    async def create_example(self, data: ExampleCreateSchema) -> Example:
        example = Example(**data.model_dump())
        self.session.add(example)
        await self.session.commit()
        await self.session.refresh(example)

        return example
