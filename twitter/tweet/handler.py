from os import write
from typing import Dict
import logging
log = logging.getLogger(__name__)

from tars.twitter.tweet.interface import TweetInterface
from tars.db.insert import Insert
from tars.utils import write_data_to_json

from sqlalchemy.exc import IntegrityError


class TweetHandler():
    def __init__(self, tweet_dict:Dict, write:bool = False):
        self.tweet = TweetInterface(tweet_dict=tweet_dict)
        if write:
            fp = f"/montebello/twitter/{tweet_dict['user']['id']}/tweets/{tweet_dict['id']}.json"
            write_data_to_json(data = tweet_dict, json_fp='/montebello/twitter/{')

    def db_load_tweet(self):
            try:
                Insert(database="twitter", table="tweets_log").load(data=self.tweet.facts)
            except IntegrityError as e:
                log.error(e)

    def db_load_quoted_tweet(self):
            quoted_tweet_dict = self.tweet.tweet_dict.get('quoted_status', None)
            if quoted_tweet_dict:
                quoted_tweet = TweetInterface(quoted_tweet_dict)
                try:
                    Insert(database="twitter", table="quoted_tweets_log").load(data=quoted_tweet.facts)
                except IntegrityError as e:
                    log.error(e)
