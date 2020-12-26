import os
import yaml

from tweepy import OAuthHandler

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class Authenticate():
    def __init__(self):
        config_fp = os.path.join(BASE_PATH, 'config.yaml')
        with open(config_fp, 'r') as (f):
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        for key, val in self.config.items():
            setattr(self, key, val)

    def get_oauth_handler(self) -> OAuthHandler:
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(
            self.access_token,
            self.access_token_secret
        )

        return auth
