import os, requests

MASTO_URL = os.environ.get("MASTO_INSTANCE") # e.g. https://mstdn.social
MASTO_TOKEN = os.environ.get("MASTO_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def get_groq_reply(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    prompt = f"Reply technically to this mastodon post about AI: '{text}'. Max 140 chars. Be helpful."
    resp = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
    return resp.json()['choices'][0]['message']['content']

def main():
    headers = {"Authorization": f"Bearer {MASTO_TOKEN}"}
    # Search for hashtag
    r = requests.get(f"{MASTO_URL}/api/v2/search", headers=headers, params={"q": "AIsecurity", "type": "statuses", "limit": 5})
    statuses = r.json().get('statuses', [])

    for status in statuses:
        if status['replies_count'] > 2: continue # Bheed mein nahi bolna
        
        reply_text = get_groq_reply(status['content'])
        # Post Reply
        requests.post(f"{MASTO_URL}/api/v1/statuses", headers=headers, json={"status": f"@{status['account']['acct']} {reply_text}", "in_reply_to_id": status['id']})
        print(f"Replied on Mastodon to {status['id']}")
        break 

if __name__ == "__main__":
    main()
