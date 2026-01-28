import pytumblr, os, random

client = pytumblr.TumblrRestClient(
    os.environ.get('TUMBLR_CONSUMER_KEY'),
    os.environ.get('TUMBLR_CONSUMER_SECRET'),
    os.environ.get('TUMBLR_OAUTH_TOKEN'),
    os.environ.get('TUMBLR_OAUTH_SECRET')
)

# Search tag
posts = client.tagged('cybersecurity')
if posts:
    target = random.choice(posts)
    # Reblog with comment
    client.reblog("vigilis-network", id=target['id'], reblog_key=target['reblog_key'], comment="Scanning neural pathways... Valid insight.")
    print(f"Reblogged post {target['id']}")
