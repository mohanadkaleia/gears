import os


def get_config():
    env = os.getenv("env") or os.getenv("ENV")

    if env and env.lower() == "production":
        config = {"SITEURL": "http://dklube.com", "SITENAME": "DKLube & Detail"}
    else:
        config = {"SITEURL": "http://localhost:5000", "SITENAME": "DKLube & Detail"}

    return config
