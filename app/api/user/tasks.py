import httpx

from app.core.config import settings
from app.email.mail import GmailSender


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


async def update_username_in_social(user_id, username):
    async with httpx.AsyncClient() as client:
        url = f"{settings.social_base_url}api/update/username"
        await client.post(url=url, json={"user_id": user_id, "username": username})


async def send_mail(
    subject: str = None,
    message: str = None,
    recipient_list: list = [],
    from_email=None,
    fail_silently=False,
    html_message=None,
    template_path=None,
):
    print(type(message))
    # GmailSender.send_mail(
    #     subject=subject[0],
    #     message=message[0],
    #     recipient_list=recipient_list,
    # )
    GmailSender.send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
    )
