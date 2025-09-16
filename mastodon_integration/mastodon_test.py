from mastodon_service import MastodonService

access_token = "3LQQJYrmIsz_vh29jW0RWy1hep798JL3qICviZaOnc0"
api_base_url = "http://localhost:3000"

if __name__ == "__main__":
    # Initialize Mastodon service
    mastodon = MastodonService(api_base_url=api_base_url, access_token=access_token)

    # Post an event announcement
    mastodon.post_event_announcement("Jazz Night", "2025-09-15", "The Hall")

    # Post simulated attendee chatter
    mastodon.post_attendee_chatter("Jazz Night", num_posts=2)

    print("✅ Test posts sent!")