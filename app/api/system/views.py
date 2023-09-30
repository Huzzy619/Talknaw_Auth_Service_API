from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.system.schema import StatusCheck
from app.email.mail import GmailSender

router = APIRouter(tags=["System"])


@router.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@router.get("/status")
async def health_status_check() -> StatusCheck:
    return {"status": True, "detail": "API is up and running "}


@router.get("/email")
def send_email():
    message = """
App passwords help you sign in to your Google Account on older apps and services that don’t support modern security standards.

App passwords are less secure than using up-to-date apps and services that use modern security standards. Before you create an app password, you should check to see if your app needs this in order to sign in.

        """
    GmailSender.send_mail(
        subject="Something about Google App Passwords",
        message=message,
        recipient_list=[
            "bd685211175@beaconmessenger.com",
            "caubeubraxauno-7044@yopmail.com",
        ],
        fail_silently=False,
    )

    return {
        "detail": "Email sent",
        "status": True,
    }
