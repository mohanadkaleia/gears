import os
import dotenv

# Read from .env file if exist
dotenv.load_dotenv()
ENV = os.getenv("env") or os.getenv("ENV")

# Development env variables (this include local)
dev = {
    "SITEURL": "http://localhost:5000",
    "SITENAME": "DKLube & Detail",
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
    "TO_EMAIL_ADDRESS": "ms.kaleia@gmail.com",
    "BCC_ENAIL_ADDRESS": "ms.kaleia@gmail.com",
}

# Production env variables
prod = {
    "SITEURL": "http://dklube.com",
    "SITENAME": "DKLube & Detail",
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
    "TO_EMAIL_ADDRESS": "dklube63@gmail.com",
    "BCC_ENAIL_ADDRESS": "ms.kaleia@gmail.com",
}


def get_config():
    if ENV and ENV.lower() == "production":
        return prod
    else:
        return dev
