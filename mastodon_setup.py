from mastodon import Mastodon
Mastodon.create_app(
    'event_management_system_app',
    api_base_url='https://cyberlab.mastodon',
    to_file='clientcred.secret'
)