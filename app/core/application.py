from fastapi import FastAPI

from app.api.example.views import router as example_router
from app.api.user.views import router as user_router 


async def  initialize():

    ...

def get_app():
    api = FastAPI()


    # api.include_router(example_router)
    api.include_router(user_router)

    @api.on_event("startup")
    async def startup_event():
        await initialize()
    


    return api
