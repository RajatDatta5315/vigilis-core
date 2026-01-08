import smtplib
from email.mime.text import MIMEText
import time
import os
try:
    from googlesearch import search
except ImportError:
    print("Google Search module not found. Install googlesearch-python")
    search = []

# CONFIG
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

# EMAIL TEMPLATE
def send_cold_email(target_email, domain):
    subject = f"Is {domain}'s AI Chatbot hallucinating?"
    body = f"""
    Hi Team {domain},
    
    I noticed you are running an AI Chatbot on your site.
    
    We recently scanned 500+ AI agents and found that 12% were hallucinating (giving wrong info) without the owners knowing.
    
    We built VIGILIS - A Free Tool to monitor your AI for hallucinations 24/7.
    
    It's free for KRYV members.
    Check your bot's health here: https://vigilis.kryv.network/
    
    Best,
    The Vigilis Team
    Powered by KRYV
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
        print(f"✅ Sent invite to {target_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send to {target_email}: {e}")
        return False

def main():
    if not EMAIL_USER: 
        print("No Email Credentials.")
        return

    print("🔎 Hunting for AI Chatbots...")
    
    # 1. SEARCH GOOGLE for targets
    # Query finds sites that likely use AI support bots
    query = '"Powered by AI" "Customer Support" contact email'
    
    targets = []
    try:
        # Get top 5 results per run to avoid spamming/blocking
        for url in search(query, num_results=5):
            domain = url.split("//")[-1].split("/")[0]
            # Construct a guess email (Cold Outreach Standard)
            # We target info@ or support@
            target_email = f"support@{domain.replace('www.', '')}"
            targets.append((domain, target_email))
    except Exception as e:
        print(f"Search Error: {e}")

    # 2. SEND EMAILS
    for domain, email in targets:
        print(f"Targeting: {domain}...")
        send_cold_email(email, domain)
        time.sleep(5) # Wait to be polite

if __name__ == "__main__":
    main()
