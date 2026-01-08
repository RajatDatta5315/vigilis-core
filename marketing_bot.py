import smtplib
from email.mime.text import MIMEText
import os
import requests

# CONFIG
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

def send_cold_email(target_email, domain):
    subject = f"Security Vulnerability in {domain}'s AI?"
    body = f"""
    Hi Team {domain},
    
    We scan AI agents for hallucinations.
    Check yours for free: https://vigilis.kryv.network
    
    - Vigilis Security
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = target_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ SENT to {target_email}")
    except Exception as e:
        print(f"❌ FAILED {target_email}: {e}")

def main():
    print("🔎 Marketing Bot Started...")
    
    # TEST MODE: Manual List (Because Google blocks Cloud IPs)
    # Add 2-3 emails here to TEST if sending works.
    # REPLACE WITH YOUR OWN ALTERNATE EMAILS FOR TEST
    targets = [
        ("TestCorp", "rajatdatta099@gmail.com"), 
        ("DemoAI", "vigilis.kryv@gmail.com")
    ]
    
    print(f"🎯 Targets Found: {len(targets)}")
    
    for domain, email in targets:
        send_cold_email(email, domain)

if __name__ == "__main__":
    main()
