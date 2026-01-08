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
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") # Built-in Action Token

def generate_professional_email(repo_name, owner_name):
    """Uses Groq to write a Context-Aware B2B Email"""
    if not GROQ_API_KEY:
        return f"Subject: Security check for {repo_name}\n\nHi {owner_name},\n\nI saw your AI project {repo_name}. You can check its safety for free at https://vigilis.kryv.network\n\n- Vigilis Team"
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    # PROMPT: Professional, Relatable, Not Spammy
    prompt = f"""
    Write a cold email to {owner_name}, the developer of an AI project named '{repo_name}'.
    
    Context: You are a fellow developer who built 'Vigilis' (a security tool).
    Observation: You noticed many AI agents leak data or hallucinate.
    Offer: A free 30-day pass to monitor '{repo_name}' using Vigilis. No credit card needed.
    Tone: Professional, concise (under 80 words), respectful.
    Link: https://vigilis.kryv.network
    
    Output Format:
    Subject: [Write a catchy subject]
    Body: [Write the body]
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
        return f"Subject: AI Safety for {repo_name}\n\nHi {owner_name},\n\nCheck {repo_name} for hallucinations using Vigilis: https://vigilis.kryv.network"

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
    print("🔎 Scanning GitHub for AI Bot Owners...")
    
    if not GITHUB_TOKEN:
        print("❌ No GitHub Token found.")
        return

    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # SEARCH QUERY: Recently updated Chatbots/AI agents
    query = "topic:chatbot topic:ai-agent pushed:>2024-01-01"
    search_url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc&per_page=20"
    
    try:
        resp = requests.get(search_url, headers=headers)
        repos = resp.json().get('items', [])
    except Exception as e:
        print(f"❌ GitHub Search Failed: {e}")
        return

    sent_count = 0
    MAX_EMAILS = 5 # Safety Limit

    for repo in repos:
        if sent_count >= MAX_EMAILS: break
        
        owner_url = repo['owner']['url']
        repo_name = repo['name']
        
        # Get Owner Details (to find email)
        try:
            user_resp = requests.get(owner_url, headers=headers)
            user_data = user_resp.json()
            
            email = user_data.get('email')
            name = user_data.get('name') or user_data.get('login')
            
            # Filter: Must have public email & be a User (not Organization)
            if email and user_data['type'] == 'User':
                print(f"🎯 Found Target: {name} (Project: {repo_name})")
                
                # Generate AI Content
                email_content = generate_professional_email(repo_name, name)
                
                # Parse Subject/Body
                if "Subject:" in email_content:
                    parts = email_content.split("Body:")
                    subject = parts[0].replace("Subject:", "").strip()
                    body = parts[1].strip() if len(parts) > 1 else parts[0]
                else:
                    subject = f"Question about {repo_name}"
                    body = email_content

                # Send
                if send_email(email, subject, body):
                    print(f"✅ Email Sent to {email}")
                    sent_count += 1
                    time.sleep(10) # Polite delay
            
        except:
            continue

    print(f"🏁 Marketing Run Complete. Emails Sent: {sent_count}")

if __name__ == "__main__":
    hunt_github_leads()
