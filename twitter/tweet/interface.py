import os, time, json
import logging
log = logging.getLogger(__name__)


base_path = os.path.dirname(os.path.realpath(__file__))

class TweetInterface():
    def __init__(self, tweet_dict):
        self.tweet_dict = tweet_dict
        self.retweet_id = self.tweet_dict.get('retweeted_status', {}).get('id')
        self.quoted_tweet_id = self.tweet_dict.get('quoted_status', {}).get('id')

        self.parse_data()

    def string_to_date(self, created_at):
        dt = time.strftime('%Y-%m-%d %H:%M:%S',
            time.strptime(
                created_at,
                '%a %b %d %H:%M:%S +0000 %Y'
            )
        )
        return(dt)

    def fact_vars(self):
        try:
            tweet_text = self.tweet_dict["extended_tweet"]['full_text']
        except:
            tweet_text = self.tweet_dict['text']

        self.facts = {
            "created_at": self.string_to_date(self.tweet_dict['created_at']),
            "user_id": self.tweet_dict['user']['id'],
            "tweet_id": self.tweet_dict['id'],
            "retweet_id": self.retweet_id,
            "quoted_tweet_id": self.quoted_tweet_id,
            "lang": self.tweet_dict['lang'],
            "source": self.tweet_dict['source'],
            "full_text": tweet_text,
            "retweet_count": self.tweet_dict.get('retweet_count', None),
            "favorite_count": self.tweet_dict.get('favorite_count', None)
        }

    def hashtag_vars(self):
        self.hashtags = []
        for hashtag in self.tweet_dict['entities']['hashtags']:
            self.hashtags.append((
                self.tweet_dict['user']['id'],
                self.tweet_dict['id'],
                hashtag['text']
            ))

    def url_vars(self):
        self.urls = []
        for url in self.tweet_dict['entities']['urls']:
            self.urls.append((
                self.tweet_dict['user']['id'],
                self.tweet_dict['id'],
                url['expanded_url']
            ))

    def user_mention_vars(self):
        self.user_mentions = []
        for user_mention in self.tweet_dict['entities']['user_mentions']:
            self.user_mentions.append((
                self.tweet_dict['user']['id'],
                self.tweet_dict['id'],
                user_mention['name'],
                user_mention['screen_name']
            ))

    def user_vars(self):
        u = self.tweet_dict['user']
        self.user = (
            self.string_to_date(u['created_at']),
            u.get('description'),
            u.get('favourites_count'),
            u.get('followers_count'),
            u.get('friends_count'),
            u.get('geo_enabled'),
            u.get('id'),
            u.get('listed_count'),
            u.get('location'),
            u.get('name'),
            u.get('profile_background_image_url'),
            u.get('profile_image_url_https'),
            u.get('screen_name'),
            u.get('statuses_count'),
            u.get('url'),
            u.get('verified')
        )

    def parse_data(self):
        self.fact_vars()
        self.hashtag_vars()
        self.url_vars()
        self.user_mention_vars()
        self.user_vars()

    def print_data(self):
        print('-------------------------- FACTS ------------------------------')
        print(self.facts)
        print('-------------------------- HASHTAGS ---------------------------')
        print(self.hashtags)
        print('-------------------------- URLS -------------------------------')
        print(self.urls)
        print('-------------------------- USER MENTIONS ----------------------')
        print(self.user_mentions)
        print('\n')

