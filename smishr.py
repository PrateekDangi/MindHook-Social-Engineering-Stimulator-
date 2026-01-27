import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE")

print("ACCOUNT_SID:", ACCOUNT_SID)
print("AUTH_TOKEN:", AUTH_TOKEN)
print("TWILIO_PHONE:", TWILIO_PHONE_NUMBER)

def send_sms(phone: str, message: str):
    print("Sending to:", phone)
    print("Message:", message)

    url = f'https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json'
    payload = {
        'To': phone,
        'From': TWILIO_PHONE_NUMBER,
        'Body': message
    }

    try:
        response = requests.post(url, data=payload, auth=HTTPBasicAuth(ACCOUNT_SID, AUTH_TOKEN))
        print("Status:", response.status_code)
        print("Response:", response.text)
        if response.status_code == 201:
            return "✅ SMS sent successfully via Twilio."
        else:
            return f"❌ Twilio Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"


# === Predefined SMS Templates ===

def get_bank_template():
    return (
        "Dear customer, your account has been temporarily suspended due to suspicious activity. "
        "Verify your identity immediately at http://verify-bank.com to avoid permanent suspension."
    )

def get_lottery_template():
    return (
        "🎉 Congratulations! You've won ₹10,00,000 in the Lucky Draw 2025. "
        "To claim your prize, visit http://claim-lottery2025.com now!"
    )

def get_default_template():
    return (
        "Important notice! Please review your recent account activity immediately. "
        "Visit http://alert-check.com to verify."
    )
