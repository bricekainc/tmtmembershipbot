from dotenv import load_dotenv
import os

load_dotenv()

# Master Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID")) # Ensure it's an integer

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Security Configuration
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()

# Conversion Rate
USD_TO_KES_RATE = 150.0

# M-Pesa ShortCode Type mapping for clarity
MPESA_SHORTCODE_TYPE = {
    "PAYBILL": "PAYBILL",
    "TILL_NUMBER": "TILL NUMBER"
}
