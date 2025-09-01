from mastodon import Mastodon
import random

# Connect to a Mastodon instance
def connect(api_base_url, access_token):
    return Mastodon(
        access_token=access_token,
        api_base_url=api_base_url
    )

# Post a new event announcement
def post_event(mastodon, event_name, date, venue):
    msg = f"🎉 New Event: {event_name} at {venue} on {date}! #CyberlabEvents"
    return mastodon.toot(msg)

# Simulate attendees posting about an event
def post_chatter(mastodon, event_name, num_posts=3):
    chatter = [
        f"Can't wait for {event_name}! 😍",
        f"{event_name} is going to be amazing! 🎶",
        f"Who else is going to {event_name}? 🙌",
        f"Bought my tickets for {event_name} already!",
        f"See you all at {event_name} 🔥"
    ]
    posts = []
    for _ in range(num_posts):
        msg = random.choice(chatter)
        posts.append(mastodon.toot(msg))
    return posts