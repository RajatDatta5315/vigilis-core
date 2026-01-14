import os
import requests
import random
from atproto import Client, models

# CONFIG
BSKY_HANDLE = os.environ.get("BSKY_HANDLE") # e.g. vigilis.bsky.social
BSKY_PASSWORD = os.environ.get("BSKY_PASSWORD")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Client()

def generate_value_post(context="trending"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"Write a very short, helpful tip (max 200 chars) for AI developers about {context}. Focus on security or preventing hallucinations. No hashtags, no sales speech. Just value."
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 80
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload)
        return resp.json()['choices'][0]['message']['content'].strip()
    except:
        return "Pro Tip: Always sanitize your AI agent's system prompts to avoid prompt injection."

def run_bluesky_promo():
    try:
        client.login(BSKY_HANDLE, BSKY_PASSWORD)
        
        # 1. Create a Value Post
        text = generate_value_post("AI Agent Security")
        client.send_post(text=text)
        print(f"✅ Posted to Bluesky: {text}")
        
        # 2. Interaction (Like/Reply to AI topics)
        # Note: Simple search and like for now
        search = client.app.bsky.feed.get_timeline() # Simplest way to get fresh feed
        for post in search.feed[:3]:
            client.like(post.post.uri, post.post.cid)
            print(f"❤️ Liked post from {post.post.author.handle}")
            
    except Exception as e:
        print(f"❌ Bluesky Error: {e}")

if __name__ == "__main__":
    run_bluesky_promo()
