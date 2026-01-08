import smtplib
from email.mime.text import MIMEText
import time
import os
import random

try:
    from googlesearch import search
except ImportError:
    print("Google Search module not found.")
    search = None

# CONFIG
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

def send_cold_email(target_email, domain):
    subject = f"Security Alert for {domain}'s AI Agent"
    
    # Randomizing templates to avoid Spam Filters
    templates = [
        f"Hi Team {domain},\n\nWe noticed you use an AI Chatbot. We scan AI agents for hallucinations (wrong answers). Check your bot's health for free at: https://vigilis.kryv.network\n\n- Vigilis Team",
        f"Hello {domain},\n\nIs your AI chatbot giving safe answers? We built a free tool to test it. No signup required for the scan: https://vigilis.kryv.network\n\n- The Vigilis Project"
    ]
    
    body = random.choice(templates)
    
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
        print(f"✅ Email sent to {target_email}")
        return True
    except Exception as e:
        print(f"❌ Failed ({target_email}): {e}")
        return False

def main():
    if not EMAIL_USER or not search: 
        print("Missing Email Credentials or Search Module.")
        return

    print("🔎 Hunting for AI Chatbots...")
    
    # Search Query
    query = '"Powered by AI" "Customer Support" contact email'
    
    count = 0
    # LIMIT: Only check top 10 results, send max 5 emails
    try:
        for url in search(query, num_results=10, lang="en"):
            if count >= 5: break # SAFETY LIMIT: 5 Emails per day
            
            try:
                # Extract Domain
                domain = url.split("//")[-1].split("/")[0].replace("www.", "")
                
                # Guess Email (Standard Support Email)
                target_email = f"support@{domain}"
                
                print(f"Targeting: {domain}...")
                success = send_cold_email(target_email, domain)
                
                if success:
                    count += 1
                    time.sleep(10) # Wait 10 seconds between emails (Anti-Spam)
            except:
                continue
                
    except Exception as e:
        print(f"Search Blocked/Error: {e}")

if __name__ == "__main__":
    main()
