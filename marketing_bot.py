import smtplib
from email.mime.text import MIMEText
import time
import os
import requests

try:
    from googlesearch import search
except ImportError:
    print("Google Search module not found.")
    search = None

# CONFIG
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_smart_email(domain):
    """Uses Groq to write a personalized cold email"""
    if not GROQ_API_KEY:
        return f"Hi Team {domain},\n\nCheck your AI chatbot for errors at https://vigilis.kryv.network\n\n- Vigilis"
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    # Prompt engineering for high conversion
    prompt = f"""
    Write a short, professional cold email to the owner of {domain}.
    Context: We noticed they are using an AI Chatbot.
    Problem: AI chatbots often 'hallucinate' (give wrong info) which hurts brand reputation.
    Solution: Invite them to use 'Vigilis' (a free tool powered by KRYV) to scan their bot.
    Link: https://vigilis.kryv.network
    Tone: Helpful, B2B, not spammy. Under 70 words.
    Subject Line: [Insert Subject Here]
    Body: [Insert Body Here]
    """
    
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload)
        content = resp.json()['choices'][0]['message']['content'].strip()
        return content
    except Exception as e:
        print(f"Groq Error: {e}")
        return f"Subject: AI Safety Check\n\nHi Team {domain},\n\nIs your AI chatbot giving accurate answers? Check it for free at https://vigilis.kryv.network"

def send_cold_email(target_email, domain):
    # 1. Generate AI Content
    ai_content = generate_smart_email(domain)
    
    # Parse Subject and Body (Simple split assumption)
    if "Subject:" in ai_content:
        parts = ai_content.split("Body:")
        subject = parts[0].replace("Subject:", "").strip()
        body = parts[1].strip() if len(parts) > 1 else parts[0]
    else:
        subject = f"Question about {domain}'s AI"
        body = ai_content

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
        print(f"✅ AI Email sent to {target_email}")
        return True
    except Exception as e:
        print(f"❌ Failed ({target_email}): {e}")
        return False

def main():
    if not EMAIL_USER or not search: 
        print("Missing Config.")
        return

    print("🔎 AI Hunting Started...")
    
    # Query: Targeted at businesses using Intercom/Zendesk/AI
    query = '"Powered by AI" "Contact Us" site:.com'
    
    count = 0
    try:
        # Search 10, Email 5 (Safety Limit)
        for url in search(query, num_results=10, lang="en"):
            if count >= 5: break 
            
            try:
                domain = url.split("//")[-1].split("/")[0].replace("www.", "")
                target_email = f"support@{domain}" # Guessing standard email
                
                print(f"Target: {domain}...")
                success = send_cold_email(target_email, domain)
                
                if success:
                    count += 1
                    time.sleep(15) # Polite delay
            except:
                continue
                
    except Exception as e:
        print(f"Search Error: {e}")

if __name__ == "__main__":
    main()
