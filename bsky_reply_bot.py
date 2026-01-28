import os, requests, random, time
from atproto import Client, models

BSKY_HANDLE = os.environ.get("BSKY_HANDLE")
BSKY_PASSWORD = os.environ.get("BSKY_PASSWORD")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def get_groq_reply(post_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Context: A user posted '{post_text}'. Task: Write a helpful, technical 1-sentence reply about AI safety/security. No sales. No emojis."
    try:
        resp = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
        return resp.json()['choices'][0]['message']['content'].strip().replace('"', '')
    except: return None

def main():
    client = Client()
    client.login(BSKY_HANDLE, BSKY_PASSWORD)
    print("SEARCHING FOR CONVERSATIONS...")
    
    # Search keywords
    data = client.app.bsky.feed.search_posts(q='AI security OR LLM hallucination', limit=5)
    
    for post in data.posts:
        if post.author.handle == BSKY_HANDLE: continue # Apne aap ko reply nahi karna
        
        # Check logic to avoid spamming same person (Optional implementation)
        reply_text = get_groq_reply(post.record.text)
        
        if reply_text:
            print(f"Replying to {post.author.handle}: {reply_text}")
            # Reply structure for Bluesky
            parent = models.create_strong_ref(post)
            root = models.create_strong_ref(post) 
            client.send_post(text=reply_text, reply=models.AppBskyFeedPost.ReplyRef(parent=parent, root=root))
            break # Sirf 1 reply per run taaki account safe rahe

if __name__ == "__main__":
    main()
