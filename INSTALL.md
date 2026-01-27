# ⚙️ SeSim – Installation & Run Guide

This guide explains how to set up and run SeSim locally.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/SeSim.git
cd SeSim


## 2️⃣ Create Virtual Environment (Recommended)

python -m venv venv

Activate Virtual Environment

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Email (Optional – for phishing mails)

Edit backend/mailer.py:

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"

⚠️ Important:
Use App Passwords, not real email passwords.
▶️ Running the Project

Start the FastAPI server:

uvicorn backend.main:app --reload

🌐 Access URLs

    Phishing Simulator
    http://127.0.0.1:8000/phishing

    Smishing Simulator
    http://127.0.0.1:8000/smishing

    Logs Viewer
    http://127.0.0.1:8000/logs/phishing

    http://127.0.0.1:8000/logs/smishing
