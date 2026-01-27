# ⚙️ SeSim – Installation & Run Guide

This guide explains how to set up and run SeSim locally.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/SeSim.git
cd SeSim
```
---

## 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Email (Optional – for phishing mails)
Edit backend/mailer.py:
```bash
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"
```
