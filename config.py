import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_URL = os.getenv("LIKECARD_BASE_URL")

EMAIL = os.getenv("LIKECARD_EMAIL")
DEVICE_ID = os.getenv("LIKECARD_DEVICE_ID")
SECURITY_CODE = os.getenv("LIKECARD_SECURITY_CODE")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 15))
