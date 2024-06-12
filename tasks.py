import os
import requests
from requests.models import Response
from typing import Dict
from dotenv import load_dotenv
load_dotenv()


def send_simple_message(to: str, subject: str, body: Dict[str, str]) -> Response:
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd684c195d8c24023b0880fd60abab6fb.mailgun.org/messages",
        auth=("api", os.getenv("API_KEY")),
        data={
            "from": "Viktor Maksimov <mailgun@YOUR_DOMAIN_NAME>",
            "to": [to],
            "subject": subject,
            "text": body,
        },
    )


def send_user_registration_email(email: str, username: str) -> object:
    return send_simple_message(
        email,
        "Succsefully signed up!",
        f"Hello, {username}, you have created an account!",
    )
