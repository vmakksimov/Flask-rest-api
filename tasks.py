
import requests
def send_simple_message(to, subject, body):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd684c195d8c24023b0880fd60abab6fb.mailgun.org/messages",
        auth=("api", "a9e96870745c05e724c7c9e65399ac2f-0a688b4a-861cf1c5"),
        data={"from": "Viktor Maksimov <mailgun@YOUR_DOMAIN_NAME>",
              "to": [to],
              "subject": subject,
              "text": body})

def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Succsefully signed up!",
        f"Hello, {username}, you have created an account!"
    )