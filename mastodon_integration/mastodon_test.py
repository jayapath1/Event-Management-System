from mastodon_client import connect, post_event, post_chatter

# Replace with your testing credentials
API_BASE_URL = "https://cyberlab.mastodon"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

if __name__ == "__main__":
    mastodon = connect(API_BASE_URL, ACCESS_TOKEN)

    # Test posting an event
    post_event(mastodon, "Jazz Night", "2025-09-15", "The Hall")

    # Test attendee chatter
    post_chatter(mastodon, "Jazz Night", num_posts=2)

    print("✅ Test posts sent!")
