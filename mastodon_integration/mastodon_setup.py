from mastodon import Mastodon
import json
import os

CONFIG_FILE = "config.json"
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError("config.json not found. Please create it with Mastodon URL and admin token.")

with open(CONFIG_FILE) as f:
    config = json.load(f)

MASTODON_BASE_URL = config.get("MASTODON_BASE_URL")
ADMIN_ACCESS_TOKEN = config.get("MASTODON_ADMIN_TOKEN")

# Eventmanager credentials
EVENTMANAGER_USERNAME = "eventmanager"
EVENTMANAGER_EMAIL = "EventManager@localhost"
EVENTMANAGER_PASSWORD = "EventManager"

mastodon = Mastodon(
    access_token=ADMIN_ACCESS_TOKEN,
    api_base_url=MASTODON_BASE_URL
)

# Checks if user exists already
existing_users = mastodon.admin_accounts()
usernames = [u.username for u in existing_users]

if EVENTMANAGER_USERNAME in usernames:
    print(f"✅ User '{EVENTMANAGER_USERNAME}' already exists.")
else:
    # Create the user
    mastodon.admin_create_account(
        username=EVENTMANAGER_USERNAME,
        email=EVENTMANAGER_EMAIL,
        password=EVENTMANAGER_PASSWORD,
        confirmed=True
    )
    print(f"✅ User '{EVENTMANAGER_USERNAME}' created successfully.")