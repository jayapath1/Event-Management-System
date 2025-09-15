from mastodon import Mastodon

mastodon = Mastodon(
    access_token="2dRSyE8p5RhhvlNo49L81eDvFdY3vUQYt1X8PSoSdKQ",
    api_base_url="http://localhost:3000"
)

mastodon.toot("Hello from Event Management System 🚀")