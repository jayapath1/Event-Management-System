Overview
The Event Management System (EMS) integrates with a Mastodon server to simulate event advertising and attendee chatter.
    - Event announcements are automatically posted when new events are created or ticket milestones are reached.
    - Simulated attendees post reactions/comments about events.
    - This allows the system to mimic real-world social media activity for testing and demonstration purposes.

Prerequisites
Access to Mastodon server (Cyberlab instance)
    - URL: http://<CYBERLAB_MASTODON_URL>
    - API access token: <INSERT_TOKEN_HERE>

[Admin/EMS UI] 
    └──> [Backend: Event Created]
            └──> [DB: Save Event]
            └──> [Mastodon API: Post New Event]
                  └──> [Store Post ID in Event Record]

[Ticket Purchase]
    └──> [Backend: Ticket Count Updated]
            └──> [Trigger if multiple of 10]
            └──> [Mastodon API: Post Chatter]

[Event Status = Live]
    └──> [Backend: Event Update]
            └──> [Mastodon API: Post Chatter Series]

[Event Status = Completed]
    └──> [Backend: Event Update]
            └──> [Mastodon API: Post Wrap-Up]

References
Getting started with the API - Mastodon documentation 2025, Joinmastodon.org, viewed 1 September 2025, <https://docs.joinmastodon.org/client/intro/>.
Mastodon.py — Mastodon.py 2.1.2 documentation 2016, Readthedocs.io, viewed 1 September 2025, <https://mastodonpy.readthedocs.io/en/stable/>.