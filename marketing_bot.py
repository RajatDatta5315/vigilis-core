import smtplib
from email.mime.text import MIMEText
import os
import requests
import time
import json

# CONFIG
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") 

def generate_professional_email(repo_name, owner_name):
    """Uses Groq to write a Context-Aware B2B Email"""
    if not GROQ_API_KEY:
        return f"Subject: Security check for {repo_name}\n\nHi {owner_name},\n\nI saw your AI project {repo_name}. Check its safety for free at https://vigilis.kryv.network\n\n- Vigilis Team"
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    Write a cold email to {owner_name}, developer of AI project '{repo_name}'.
    Context: You built 'Vigilis', a security tool for AI agents.
    Observation: AI agents often hallucinate.
    Offer: Free 30-day monitor for '{repo_name}'.
    Tone: Professional, short (under 80 words), no fluff.
    Link: https://vigilis.kryv.network
    
    Output Format:
    Subject: [Subject]
    Body: [Body]
    """
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload)
        content = resp.json()['choices'][0]['message']['content'].strip()
        return content
    except:
        return f"Subject: Safety Scan for {repo_name}\n\nHi {owner_name},\n\nCheck {repo_name} for hallucinations: https://vigilis.kryv.network"

def send_email(target_email, subject, body):
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
        return True
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False

def hunt_github_leads():
    print("🔎 Scanning GitHub (Deep Scan 100 Repos)...")
    
    if not GITHUB_TOKEN:
        print("❌ No GitHub Token.")
        return

    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # INCREASED SCAN LIMIT TO 100
    query = "topic:chatbot topic:ai-agent pushed:>2024-01-01"
    search_url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc&per_page=100"
    
    try:
        resp = requests.get(search_url, headers=headers)
        repos = resp.json().get('items', [])
    except Exception as e:
        print(f"❌ Search Failed: {e}")
        return

    sent_count = 0
    MAX_EMAILS = 5 # Strict Safety Limit

    print(f"🔍 Found {len(repos)} updated repos. Filtering for public emails...")

    for repo in repos:
        if sent_count >= MAX_EMAILS: break
        
        owner_url = repo['owner']['url']
        repo_name = repo['name']
        
        try:
            user_resp = requests.get(owner_url, headers=headers)
            user_data = user_resp.json()
            
            email = user_data.get('email')
            name = user_data.get('name') or user_data.get('login')
            
            if email and user_data['type'] == 'User':
                print(f"🎯 Target Acquired: {name} ({repo_name})")
                
                content = generate_professional_email(repo_name, name)
                
                if "Subject:" in content:
                    parts = content.split("Body:")
                    subject = parts[0].replace("Subject:", "").strip()
                    body = parts[1].strip() if len(parts) > 1 else parts[0]
                else:
                    subject = f"Dev Question: {repo_name}"
                    body = content

                if send_email(email, subject, body):
                    print(f"✅ Sent to {email}")
                    sent_count += 1
                    time.sleep(10)
            
        except:
            continue

    print(f"🏁 Run Complete. Total Sent: {sent_count}")

if __name__ == "__main__":
    hunt_github_leads()
