import praw, os, time, random, requests

def get_groq_content():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
    prompt = "Write a high-value technical post about AI Security or protecting LLMs. Make it look like a developer sharing a tip. Max 300 words. No hashtags."
    resp = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
    return resp.json()['choices'][0]['message']['content']

def post_to_reddit():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent='Vigilis-Bot-v1.0',
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD')
    )

    subreddits = ['test', 'SideProject', 'AIExplained'] # 'test' for testing, others for reach
    content = get_groq_content()
    title = "Quick Insight: Securing Neural Pathways in AI Agents"

    for sub in subreddits:
        try:
            print(f"Posting to r/{sub}...")
            reddit.subreddit(sub).submit(title, selftext=content)
            print(f"✅ Posted to r/{sub}")
            # CRITICAL WARNING FIX: 10 min sleep between posts
            wait_time = random.randint(600, 900) 
            print(f"Waiting {wait_time} seconds to avoid shadowban...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"❌ Error in r/{sub}: {e}")

if __name__ == "__main__":
    post_to_reddit()
