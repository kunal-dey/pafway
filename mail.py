from typing import List
from utils.config import MAIL_API_KEY, REGISTERED_MAIL
from requests import Response

from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from utils.errors import MailException

FAILED_SERVER_CONNECT = "Failed to connect the MAIL server."


def send_email(email: List[str], subject, text, html) -> Response:
        message = Mail(
            from_email= REGISTERED_MAIL,
            to_emails=email, 
            subject=subject, 
            html_content=html,
            plain_text_content=text
        )

        try:
            sg=SendGridAPIClient(MAIL_API_KEY)
            response=sg.send(message)
        except Exception as e:
            raise MailException(FAILED_SERVER_CONNECT)
        return response