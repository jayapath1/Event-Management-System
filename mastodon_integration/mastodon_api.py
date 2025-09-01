from mastodon import Mastodon

mastodon = Mastodon(
    access_token="PASTE_YOUR_TOKEN_HERE",
    api_base_url="https://cyberlab.mastodon"
)

mastodon.toot("Hello from Event Management System 🚀")