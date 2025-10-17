# alerter.py
import smtplib
from email.message import EmailMessage
import os

def send_email(cfg, subject, body, attachments=None, html=False):
    """
    Send an email alert.
    cfg: dict from config.yaml 'email' section
    subject: email subject
    body: plain text or HTML body
    attachments: list of file paths
    html: bool, True if body is HTML
    """
    if not cfg.get("enabled", False):
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = cfg.get("from", cfg.get("username"))
    msg['To'] = ", ".join(cfg.get("to", []))
    
    if html:
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)

    # Attach files
    if attachments:
        for file_path in attachments:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(file_path)
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP(cfg.get("smtp_server"), cfg.get("smtp_port")) as s:
            if cfg.get("use_tls", True):
                s.starttls()
            s.login(cfg.get("username"), cfg.get("password"))
            s.send_message(msg)
            print(f"[+] Email sent: {subject}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")
