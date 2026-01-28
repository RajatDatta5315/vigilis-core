import praw, os, time, random, requests

def get_ai_reply(post_title, post_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
    
    prompt = f"""
    Context: A Reddit post titled '{post_title}' says: '{post_text[:300]}'
    Task: Write a 1-sentence helpful, technical comment about AI safety or LLM security related to this. 
    Rule: DO NOT promote any product. DO NOT use emojis. Be a helpful peer.
    """
    
    try:
        resp = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
        return resp.json()['choices'][0]['message']['content'].strip().replace('"', '')
    except:
        return None

def main():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent='Vigilis-Reply-Bot-v1.0',
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD')
    )

    # Niche subreddits for high value
    target_subs = ['LocalLLaMA', 'OpenAI', 'ArtificialInteligence']
    sub_name = random.choice(target_subs)
    print(f"Scanning r/{sub_name} for value-add opportunities...")

    count = 0
    for submission in reddit.subreddit(sub_name).hot(limit=10):
        if count >= 1: break # Sirf 1 reply per run (Safe Limit)
        
        # Check if we already replied
        submission.comments.replace_more(limit=0)
        if any(comment.author == reddit.user.me() for comment in submission.comments):
            continue

        reply_content = get_ai_reply(submission.title, submission.selftext)
        
        if reply_content:
            print(f"Replying to: {submission.title}")
            submission.reply(reply_content)
            print(f"✅ Reply posted: {reply_content}")
            count += 1
            time.sleep(10) # Small buffer

if __name__ == "__main__":
    main()
