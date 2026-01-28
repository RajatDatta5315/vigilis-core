import pytumblr, os, requests

client = pytumblr.TumblrRestClient(
    os.environ.get('TUMBLR_CONSUMER_KEY'),
    os.environ.get('TUMBLR_CONSUMER_SECRET'),
    os.environ.get('TUMBLR_OAUTH_TOKEN'),
    os.environ.get('TUMBLR_OAUTH_SECRET')
)

# Groq Generate
url = "https://api.groq.com/openai/v1/chat/completions"
prompt = "Write a short aesthetic cyberpunk style quote about AI surveillance. Max 20 words."
resp = requests.post(url, headers={"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"}, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
content = resp.json()['choices'][0]['message']['content'].replace('"', '')

# Post Text
client.create_text("vigilis-network", state="published", slug="ai-security-log", title="VIGILIS LOG", body=content, tags=["ai", "cybersecurity", "glitch"])
print("Tumblr Posted.")
