import sendgrid
from app.config import get_config


class ErrSendEmail(Exception):
    pass


_configs = get_config()
_sg = sendgrid.SendGridAPIClient(api_key=_configs["SENDGRID_API_KEY"])


def send(from_, to_, subject, body):
    data = {
        "personalizations": [{"to": [{"email": to_}], "subject": subject}],
        "from": {"email": from_},
        "content": [{"type": "text/plain", "value": body}],
    }

    response = _sg.client.mail.send.post(request_body=data)
    if response.status_code not in (200, 201, 202):
        raise ErrSendEmail(f"failed to send email with status {response.status_code}")
