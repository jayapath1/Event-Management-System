from mastodon import Mastodon
import random
from bs4 import BeautifulSoup

class MastodonService:
    def __init__(self, api_base_url: str, access_token: str):
        """
        Initialize Mastodon service with API URL and access token.
        """
        self.mastodon = Mastodon(
            access_token=access_token,
            api_base_url=api_base_url
        )

    def post_event_announcement(self, event_name: str, date: str, venue: str, ticket_link: str = None, hashtags=None):
        msg = f"🎉 New Event: {event_name} at {venue} on {date}!"
        if ticket_link:
            msg += f" Tickets: {ticket_link}"
        if hashtags:
            msg += " " + " ".join(f"#{tag}" for tag in hashtags)
        post = self.mastodon.toot(msg)
        return post.id

    def post_attendee_chatter(self, event_name: str, num_posts: int = 5, hashtags=None):
        messages = [
            f"Can't wait for {event_name}! 😍",
            f"{event_name} is going to be amazing! 🎶",
            f"Who else is going to {event_name}? 🙌",
            f"Counting down the days until {event_name}!",
            f"Excited to attend {event_name}! #CyberlabEvents"
        ]
        post_ids = []
        for _ in range(num_posts):
            msg = random.choice(messages)
            if hashtags:
                msg += " " + " ".join(f"#{tag}" for tag in hashtags)
            post = self.mastodon.toot(msg)
            post_ids.append(post.id)
        return post_ids

    def post_event_wrapup(self, event_name: str, summary_link: str = None, hashtags=None):
        msg = f"Thanks for attending {event_name}! 🎉"
        if summary_link:
            msg += f" Photos & highlights: {summary_link}"
        if hashtags:
            msg += " " + " ".join(f"#{tag}" for tag in hashtags)
        post = self.mastodon.toot(msg)
        return post.id

    def fetch_posts_by_hashtag(self, hashtag: str, limit: int = 10):
        """
        Fetch latest posts for a specific hashtag and strip HTML from content.
        """
        try:
            posts = self.mastodon.timeline_hashtag(hashtag, limit=limit)
            result = []
            for post in posts:
                content = BeautifulSoup(post["content"], "html.parser").get_text()
                result.append({
                    "user": post["account"]["username"],
                    "text": content,
                    "time": post["created_at"].isoformat()
                })
            return result
        except Exception as e:
            print(f"Error fetching posts for #{hashtag}: {e}")
            return []
