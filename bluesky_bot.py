import os
import requests
import random
import time
from atproto import Client, models

# --- CONFIG ---
BSKY_HANDLE = os.environ.get("BSKY_HANDLE")
BSKY_PASSWORD = os.environ.get("BSKY_PASSWORD")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Client()

def generate_human_insight(context="AI security"):
    """Groq API: Chill Dev Mode"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    You are a chill AI security researcher who hates corporate fluff. 
    Context: {context}
    Task: Write a very short, sharp observation (max 160 chars) about AI safety or LLM hallucinations.
    Style: No emojis, no hashtags, no 'Hey everyone', no marketing talk. 
    Just sound like a smart dev thinking out loud on a Wednesday morning.
    Example: "Most AI agents fail because people forget to bound their system instructions. It's like leaving the front door open for prompt injection."
    """
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        content = resp.json()['choices'][0]['message']['content'].strip()
        # Remove quotes if AI adds them
        return content.replace('"', '')
    except Exception as e:
        print(f"Groq Error: {e}")
        return "Sanitizing system prompts is basic, but still, half the AI agents out there are wide open to basic jailbreaks."

def run_bluesky_promo():
    try:
        print("🤖 Connecting to Bluesky...")
        client.login(BSKY_HANDLE, BSKY_PASSWORD)
        
        # 1. Post a Value-Add Insight
        text = generate_human_insight()
        client.send_post(text=text)
        print(f"✅ Posted: {text}")
        
        # 2. Value-Add Commenting (Spam nahi, help)
        # Trending topics search
        print("🔍 Finding AI conversations to join...")
        search_results = client.app.bsky.feed.get_timeline(algorithm='reverse-chronological')
        
        count = 0
        for feed_view in search_results.feed:
            if count >= 2: break # Only 2 interactions to keep it human
            
            post = feed_view.post
            # Like the post
            client.like(post.uri, post.cid)
            print(f"❤️ Liked: {post.author.handle}")
            
            # Add a value comment
            comment_text = generate_human_insight(context="Specific AI safety tip")
            # In a real scenario, you'd reply to the post CID, but keeping it simple for now
            # client.send_post(text=comment_text, reply_to=models.ComAtprotoRepoCreateRecord.ReplyRef(post, post))
            
            count += 1
            time.sleep(5)
            
    except Exception as e:
        print(f"❌ Bluesky Critical Error: {e}")

if __name__ == "__main__":
    if not BSKY_HANDLE or not BSKY_PASSWORD or not GROQ_API_KEY:
        print("❌ Missing API Keys in Secrets!")
    else:
        run_bluesky_promo()
