import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_GMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_KEY")
SMTP_SERVER = os.getenv("SMTP_URL", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def send_mail_with_files(recipients, attachments, subject=None, body_text=None, skip_missing=True):
    """
    Send email with DOCX and PDF attachments to one or multiple recipients.

    - `recipients`: list or comma-separated string
    - `attachments`: iterable of file paths (strings)
    - `subject`: optional subject string
    - `body_text`: optional plain text body
    - `skip_missing`: if True, skip files that don't exist and continue; if False, raise on missing
    Returns: list of file paths that were attached
    """

    if not SENDER_EMAIL or not APP_PASSWORD:
        raise ValueError("❌ Missing SENDER_GMAIL or GMAIL_APP_KEY in .env file")

    # Normalize recipients
    if isinstance(recipients, str):
        recipients = [r.strip() for r in recipients.split(",") if r.strip()]
    elif not isinstance(recipients, list):
        raise TypeError("Recipients must be a list or comma-separated string.")

    if not recipients:
        raise ValueError("❌ No recipients provided.")

    # Prepare message
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject or "📄 Processed Resumes (DOCX & PDF Attached)"
    body = MIMEText(
        body_text or "Hello,\n\nPlease find attached the processed resume files in both DOCX and PDF formats.\n\nBest regards,\nResume Processor",
        "plain"
    )
    msg.attach(body)

    attached_files = []
    for file_path in attachments:
        if not file_path:
            continue
        if not os.path.exists(file_path):
            msg_text = f"⚠️ Attachment not found: {file_path}"
            # Print so Streamlit / console will show missing files
            print(msg_text)
            if not skip_missing:
                raise FileNotFoundError(msg_text)
            else:
                continue

        # Basic sanity: ensure file has non-zero size
        if os.path.getsize(file_path) == 0:
            msg_text = f"⚠️ Attachment has zero bytes: {file_path}"
            print(msg_text)
            if not skip_missing:
                raise ValueError(msg_text)
            else:
                continue

        with open(file_path, "rb") as f:
            file_part = MIMEApplication(f.read(), Name=os.path.basename(file_path))

        # Suggest the correct Content-Type header for common file types (improves mail clients)
        filename = os.path.basename(file_path)
        file_part["Content-Disposition"] = f'attachment; filename="{filename}"'
        msg.attach(file_part)
        attached_files.append(file_path)
        print(f"ℹ Attached: {file_path}")

    if not attached_files:
        raise RuntimeError("❌ No attachments to send (all were missing or invalid). Email not sent.")

    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
            print(f"✅ Email successfully sent to: {', '.join(recipients)} — attached: {attached_files}")
            return attached_files
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise
