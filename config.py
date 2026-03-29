import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_URL = os.getenv("LIKECARD_BASE_URL")
API_KEY = os.getenv("LIKECARD_API_KEY")
SECRET = os.getenv("LIKECARD_SECRET")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 15))
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
