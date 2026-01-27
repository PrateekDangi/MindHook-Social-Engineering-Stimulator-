import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# === Email Validation Function ===
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# === Main Email Function for FastAPI ===
def send_email(sender_email, app_password, sender_name,
               receiver_email, user_id, subject, body_text, suspicious_link):

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Plain text fallback
    plain_text = (
        "A suspicious activity was detected.\n"
        "If you can't view this email properly, please use an HTML-supported email client."
    )

    # Attach plain + HTML versions
    part1 = MIMEText(plain_text, "plain", "utf-8")
    part2 = MIMEText(body_text, "html", "utf-8")

    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"


# === CLI TESTING MODE ===
if __name__ == "__main__":
    sender_email = input("Enter your (sender) email: ").strip()
    while not is_valid_email(sender_email):
        print("❌ Invalid email format. Try again.")
        sender_email = input("Enter sender email: ").strip()

    sender_name = input("Enter sender display name (e.g. SEsim): ").strip()
    app_password = input("Enter your app password (16 digit): ").strip()

    receiver_email = input("Enter recipient email: ").strip()
    while not is_valid_email(receiver_email):
        print("❌ Invalid email format. Try again.")
        receiver_email = input("Enter recipient email: ").strip()

    user_id = input("Enter tracking ID (e.g. user123): ").strip()
    subject = input("Enter email subject: ").strip()

    print("Enter your email body (HTML allowed): Press ENTER 3 times to finish:")
    lines = []
    empty_lines = 0
    while True:
        line = input()
        if line.strip() == "":
            empty_lines += 1
            if empty_lines == 3:
                break
        else:
            empty_lines = 0
            lines.append(line + "\n")

    body_text = "".join(lines)

    print("\nChoose suspicious link type:")
    print("1. Microsoft 365 Login Simulation")
    print("2. Google Docs Login Simulation")
    print("3. Custom Suspicious Link")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        suspicious_link = f"http://localhost:8000/track?id={user_id}&type=microsoft"
    elif choice == "2":
        suspicious_link = f"http://localhost:8000/track?id={user_id}&type=google"
    elif choice == "3":
        suspicious_link = input("Enter your custom suspicious link: ").strip()
    else:
        print("❌ Invalid choice. Exiting.")
        exit()

    # Append suspicious link to email
    body_text += f'<br><br><a href="{suspicious_link}" target="_blank" style="color:#1a73e8;">Click here to view suspicious activity</a>'

    # Send email
    result = send_email(
        sender_email, app_password, sender_name,
        receiver_email, user_id, subject, body_text, suspicious_link
    )
    print(result)
