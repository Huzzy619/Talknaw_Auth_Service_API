import smtplib
import ssl
from email.message import EmailMessage

from app.core.config import settings


class GmailSender:
    @staticmethod
    def send_mail(
        subject: str,
        message: str,
        recipient_list: list,
        from_email: str = None,
        fail_silently: bool = False,
        html_message: str = None,
        template_path: str = None,
    ):
        email = EmailMessage()
        email["from"] = from_email or settings.default_from_email
        email["to"] = recipient_list
        email["subject"] = subject
        email.set_content(message)

        print(message)

        # if html_message:
        #     email.add_alternative(html_message, subtype="html")
        # elif template_path:
        #     with open(template_path, "r") as template_file:
        #         html_content = template_file.read()
        #     email.add_alternative(html_content, subtype="html")

        # context = ssl.create_default_context()

        # try:
        #     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        #             smtp.login(settings.default_from_email, settings.email_password)
        #             smtp.send_message(email)
        # except Exception as e:
        #     if not fail_silently:
        #         raise e

    @staticmethod
    def send_mail_with_context(
        context: dict,
        from_email: str,
        recipient_list: list,
        subject: str,
        template_path: str,
    ):
        # Read the template file
        with open(template_path, "r") as template_file:
            html_template = template_file.read()

        # Apply context data to the template
        formatted_html = html_template.format(**context)

        GmailSender.send_mail(
            subject=subject,
            message="Text message content",
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=formatted_html,
        )


# Example usage:
if __name__ == "__main__":
    email_sender = "rW8XK@example.com"
    email_app_password = "password"
    email_recipient = "rW8XK@example.com"
    email_subject = "Test"
    email_body = "Test"
    template_path = "path/to/your/template.html"

    GmailSender.send_mail(
        subject=email_subject,
        message=email_body,
        from_email=email_sender,
        recipient_list=email_recipient,
        auth_user=email_sender,
        auth_password=email_app_password,
        template_path=template_path,
    )
