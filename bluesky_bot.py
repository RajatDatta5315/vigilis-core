import os
import requests
import random
import time
from atproto import Client, models

BSKY_HANDLE = os.environ.get("BSKY_HANDLE")
BSKY_PASSWORD = os.environ.get("BSKY_PASSWORD")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Client()

def generate_insight(context="general"):
    """Groq API: Value-Add Insight Generator"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    Context: {context}
    Task: Write a short (max 140 chars) insight about AI security or preventing hallucinations.
    Rule: NO sales talk, NO hashtags, NO emojis. Just pure technical or logical value. 
    Sound like a senior dev giving a quick tip.
    """
    
    try:
        resp = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 60})
        return resp.json()['choices'][0]['message']['content'].strip().replace('"', '')
    except:
        return "Boundaries in system prompts are often overlooked but critical for agent security."

def run_social():
    try:
        client.login(BSKY_HANDLE, BSKY_PASSWORD)
        
        # 1. Post original insight
        insight = generate_insight("original thought")
        client.send_post(text=insight)
        print(f"✅ Posted insight: {insight}")

        # 2. Search & Value-Comment
        keywords = ["AI safety", "LLM hallucinations", "AI security", "Prompt injection"]
        query = random.choice(keywords)
        print(f"🔍 Searching for: {query}")
        
        search = client.app.bsky.feed.get_timeline() # Simplified for stability
        
        count = 0
        for feed_view in search.feed[:5]:
            if count >= 1: break # Commenting on 1 post per run to avoid shadowban
            
            post = feed_view.post
            if BSKY_HANDLE not in post.author.handle:
                comment = generate_insight(f"replying to a post about {query}")
                
                # Posting a reply
                parent = models.ComAtprotoRepoCreateRecord.ReplyRef(root=post, parent=post)
                client.send_post(text=comment, reply=parent)
                
                print(f"💬 Commented on {post.author.handle}: {comment}")
                count += 1
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_social()
