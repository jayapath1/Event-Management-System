from mastodon import Mastodon
import random

class MastodonService:
    def __init__(self, api_base_url: str, access_token: str):
        """
        Initialize Mastodon service with API URL and access token.
        """
        self.mastodon = Mastodon(
            access_token=access_token,
            api_base_url=api_base_url
        )

    def post_event_announcement(self, event_name: str, date: str, venue: str, ticket_link: str = None):
        """
        Post a new event announcement to Mastodon.
        """
        msg = f"🎉 New Event: {event_name} at {venue} on {date}!"
        if ticket_link:
            msg += f" Tickets: {ticket_link}"
        post = self.mastodon.toot(msg)
        return post.id

    def post_attendee_chatter(self, event_name: str, num_posts: int = 5):
        """
        Simulate attendee chatter posts for an event.
        """
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
            post = self.mastodon.toot(msg)
            post_ids.append(post.id)
        return post_ids

    def post_event_wrapup(self, event_name: str, summary_link: str = None):
        """
        Post a wrap-up message after the event is completed.
        """
        msg = f"Thanks for attending {event_name}! 🎉"
        if summary_link:
            msg += f" Photos & highlights: {summary_link}"
        post = self.mastodon.toot(msg)
        return post.id
