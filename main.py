from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import sqlite3
import db
import mailer
import shutil
import os
import smishr
import subprocess
import shlex

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Welcome to SEsim!"}

@app.get("/open")
def track_open(id: str):
    db.log_event(id, "opened", datetime.now().isoformat())
    return FileResponse("pixel.png", media_type="image/png")

@app.get("/track")
def track_click(id: str, type: str = "microsoft"):
    db.log_event(id, "clicked", datetime.now().isoformat())

    if type == "google":
        page_title = "Sign in – Google Accounts"
        logo = "https://ssl.gstatic.com/accounts/ui/logo_2x.png"
        prompt = "to continue to Google Docs"
    else:
        page_title = "Sign in to your account"
        logo = "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"
        prompt = "to continue to Microsoft 365"

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{page_title}</title>
        <style>
            body {{
                margin: 0; padding: 0; background-color: #f2f2f2;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex; align-items: center; justify-content: center; height: 100vh;
            }}
            .container {{
                background: white; padding: 40px; width: 350px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-radius: 8px;
            }}
            .logo {{ text-align: center; margin-bottom: 20px; }}
            .logo img {{ width: 130px; }}
            h2 {{ font-size: 22px; text-align: center; color: #333; margin-bottom: 10px; }}
            p {{ font-size: 13px; text-align: center; color: #666; margin-bottom: 20px; }}
            input[type="text"], input[type="password"] {{
                width: 100%; padding: 10px; margin: 10px 0;
                border: 1px solid #ccc; border-radius: 5px; font-size: 14px;
            }}
            input[type="submit"] {{
                background-color: #1a73e8; color: white;
                padding: 10px; width: 100%;
                border: none; border-radius: 5px; font-size: 16px;
                cursor: pointer; margin-top: 15px;
            }}
            input[type="submit"]:hover {{ background-color: #0c58b1; }}
            .footer {{ margin-top: 20px; font-size: 11px; color: #666; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <img src="{logo}" alt="Logo">
            </div>
            <h2>Sign in</h2>
            <p>{prompt}</p>
            <form action="/submit" method="post" onsubmit="return validateForm()">
                <input type="hidden" name="id" value="{id}">
                <label>Email</label>
                <input type="text" name="email" id="email" placeholder="someone@example.com" required>
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter your password" required>
                <input type="submit" value="Next">
            </form>
            <div class="footer">This is a simulation. Do not reuse real passwords.</div>
        </div>
        <script>
            function validateForm() {{
                const email = document.getElementById("email").value;
                const pattern = /^[\\w.-]+@[\\w.-]+\\.\\w+$/;
                if (!pattern.test(email)) {{
                    alert("❌ Please enter a valid email address.");
                    return false;
                }}
                return true;
            }}
        </script>
    </body>
    </html>
    """)

@app.post("/submit")
async def track_submit(request: Request):
    form = await request.form()
    user_id = form.get("id", "unknown")
    email = form.get("email", "N/A")
    password = form.get("password", "N/A")
    timestamp = datetime.now().isoformat()
    db.log_event(user_id, "submitted", timestamp, email, password)
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                background-color: #f3f3f3;
                font-family: Arial, sans-serif;
                display: flex; align-items: center; justify-content: center;
                height: 100vh; margin: 0;
            }
            .box {
                background-color: #fff;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
                width: 400px;
            }
            h2 { color: #1a73e8; }
            p { color: #555; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>✅ Submission Logged Successfully</h2>
            <p>This was a simulated phishing test as part of SEsim awareness training.</p>
            <p>You may now close this page.</p>
        </div>
    </body>
    </html>
    """)

@app.get("/form", response_class=HTMLResponse)
def email_form(request: Request):
    return templates.TemplateResponse("phishing_form.html", {"request": request})

@app.get("/smishing-form", response_class=HTMLResponse)
def smishing_form(request: Request):
    return templates.TemplateResponse("smishing_form.html", {"request": request})

@app.get("/cms", response_class=HTMLResponse)
def cms_page(request: Request):
    return templates.TemplateResponse("cms.html", {"request": request})

@app.post("/send-phishing", response_class=HTMLResponse)
async def send_phishing_email(request: Request, attachment: UploadFile = None):
    form = await request.form()
    sender_name = form.get("sender_name")
    sender_email = form.get("sender_email")
    app_password = form.get("app_password")
    recipient_email = form.get("recipient_email")
    user_id = form.get("user_id")
    subject = form.get("subject")
    email_type = form.get("emailType")  # 'template' or 'custom'
    link_option = form.get("link_option")
    custom_link = form.get("custom_link", "")
    editor_body = form.get("body", "")

    # === Phishing link generation
    if link_option == "google":
        phishing_link = f"http://localhost:8000/track?id={user_id}&type=google"
    elif link_option == "microsoft":
        phishing_link = f"http://localhost:8000/track?id={user_id}&type=microsoft"
    elif link_option == "custom":
        phishing_link = custom_link
    else:
        phishing_link = "#"

    # === Invisible pixel link
    open_link = phishing_link.replace("/track", "/open")

    # === Email Body (Template or Custom)
    if email_type == "template":
        if link_option == "google":
            body = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>⚠️ Security Alert</title>
            </head>
            <body style="font-family: Arial, sans-serif; background-color: #f1f1f1; padding: 40px; display: flex; justify-content: center;">
                <div style="background: white; padding: 30px; border-radius: 8px; max-width: 600px; width: 100%; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
                    <img src="https://ssl.gstatic.com/accounts/ui/logo_2x.png" alt="Google Logo" style="width: 120px; margin-bottom: 20px;">
                    <h2 style="color: #d93025;">⚠️ New Sign-in Attempt Detected</h2>
                    <p style="font-size: 16px;">We detected a suspicious login attempt to your Google Account.</p>
                    <p style="font-size: 16px;">If this was you, you can safely ignore this email. If not, please secure your account immediately.</p>
                    <a href="{phishing_link}" style="display: inline-block; margin-top: 20px; background-color: #1a73e8; color: white; padding: 12px 24px; text-decoration: none; font-size: 16px; border-radius: 5px;">Check activity</a>
                    <div style="margin-top: 15px;">
                        <a href="{phishing_link}" style="font-size: 14px; color: #1a73e8; text-decoration: underline;">Report this activity</a>
                    </div>
                    <p style="margin-top: 30px; font-size: 12px; color: #777;">This message was sent by Google Account Security Team. If you didn’t request this, someone else may be trying to access your account.</p>
                    <img src="{open_link}" width="1" height="1" style="display: none;">
                </div>
            </body>
            </html>
            """
        elif link_option == "microsoft":
            body = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>⚠️ Unusual Sign-in Activity</title>
            </head>
            <body style="font-family: Segoe UI, sans-serif; background-color: #f4f4f4; padding: 40px; display: flex; justify-content: center;">
                <div style="background: white; padding: 30px; border-radius: 8px; max-width: 600px; width: 100%; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
                    <img src="https://1000logos.net/wp-content/uploads/2021/04/Microsoft-logo.png" alt="Microsoft Logo" style="width: 140px; margin-bottom: 20px;">
                    <h2 style="color: #d93025;">⚠️ Unusual sign-in activity</h2>
                    <p style="font-size: 16px;">We detected a sign-in attempt that doesn't match your usual activity.</p>
                    <p style="font-size: 16px;">To keep your account safe, please verify the activity immediately.</p>
                    <a href="{phishing_link}" style="display: inline-block; margin-top: 20px; background-color: #0078D4; color: white; padding: 12px 24px; text-decoration: none; font-size: 16px; border-radius: 5px;">Review Activity</a>
                    <div style="margin-top: 15px;">
                        <a href="{phishing_link}" style="font-size: 14px; color: #0078D4; text-decoration: underline;">Report this activity</a>
                    </div>
                    <p style="margin-top: 30px; font-size: 12px; color: #777;">This message was sent by Microsoft Account Team. If you didn’t try to sign in, someone else might be trying to access your account.</p>
                    <img src="{open_link}" width="1" height="1" style="display: none;">
                </div>
            </body>
            </html>
            """
        else:
            body = "<p>⚠️ Unknown template type.</p>"
    else:
        body = editor_body.replace("[link]", f'<a href="{phishing_link}" target="_blank">Click here</a>')

    # === Save attachment (optional)
    attachment_path = None
    if attachment and attachment.filename:
        os.makedirs("temp_attachments", exist_ok=True)
        attachment_path = f"temp_attachments/{attachment.filename}"
        with open(attachment_path, "wb") as f:
            shutil.copyfileobj(attachment.file, f)

    # === Send Email
    result = mailer.send_email(
        sender_email, app_password, sender_name,
        recipient_email, user_id, subject, body, phishing_link
    )

    if attachment_path and os.path.exists(attachment_path):
        os.remove(attachment_path)

    return templates.TemplateResponse("phishing_form.html", {
        "request": request,
        "status": result
    })

@app.post("/send-smishing", response_class=HTMLResponse)
async def send_smishing(request: Request):
    form = await request.form()
    sender_name = form.get("sender_name_sms")
    country_code = form.get("country_code")
    phone_number = form.get("phone_number")
    full_number = f"{country_code}{phone_number}"

    message_type = form.get("smsType")
    template_option = form.get("template_option_sms")
    message_body = form.get("message_body_sms")

    if message_type == "template":
        if template_option == "bank":
            message_body = smishr.get_bank_template()
        elif template_option == "lottery":
            message_body = smishr.get_lottery_template()
        else:
            message_body = smishr.get_default_template()

    result = smishr.send_sms(full_number, message_body)
    db.log_event(
    user_id="smish",
    event="sent",
    timestamp=datetime.now().isoformat(),
    phone=full_number,
    message=message_body[:50]
    )
    
    return templates.TemplateResponse("smishing_form.html", {
        "request": request,
        "sms_status": result + " ✅ SMS sent successfully."
    })

@app.get("/logs/phishing", response_class=HTMLResponse)
def view_phishing_logs(request: Request):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, user_id, event, email, password 
        FROM logs 
        WHERE email IS NOT NULL AND phone IS NULL 
        ORDER BY timestamp DESC
    """)
    logs = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("phishing_logs.html", {"request": request, "logs": logs})


@app.get("/logs/smishing", response_class=HTMLResponse)
def view_smishing_logs(request: Request):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT event, timestamp, phone, message 
        FROM logs 
        WHERE phone IS NOT NULL 
        ORDER BY timestamp DESC
    """)
    logs = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("smishing_logs.html", {"request": request, "logs": logs})

@app.get("/cmd-exec", response_class=HTMLResponse)
def cmd_exec_page(request: Request):
    return templates.TemplateResponse("cmd_exec.html", {"request": request})

@app.post("/execute-cmd")
async def execute_command(request: Request):
    form = await request.form()
    command = form.get("command", "")
    output = "No command provided."
    error = ""

    if command:
        try:
            # Use shlex to safely split the command string
            command_list = shlex.split(command)
            # Use subprocess.run for secure execution
            result = subprocess.run(
                command_list,
                capture_output=True,
                text=True,
                check=True,
                shell=False
            )
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = e.stdout
            error = e.stderr
        except FileNotFoundError:
            error = f"Command not found: '{command_list[0]}'"
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"

    return templates.TemplateResponse("cmd_exec.html", {
        "request": request,
        "output": output,
        "error": error
    })
