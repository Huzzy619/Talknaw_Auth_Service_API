import httpx
from app.core.config import settings

async def create_profile(new_user: dict):
    user_data = {k: str(v) for k, v in new_user.items()}

    user_data.pop("access_token")
    user_data.pop("refresh_token")
    user_data.pop("password")
    user_data.pop("email")
    async with httpx.AsyncClient() as client:
        # headers = {
        #     'X-CSRFTOKEN': 'OxunMWTYw3lVtwb71qSNCar3PdwwnQapAOrZbqWz8VZON3eM0vR4hK2jtRw7PJiS'
        # }
        url = f"{settings.social_base_url}api/create/profile"

        await client.post(url=url, json=user_data)
