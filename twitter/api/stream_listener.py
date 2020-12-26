from __future__ import absolute_import, print_function

import json
import os
import logging
log = logging.getLogger(__name__)


from pathlib import Path
from tweepy import Stream, StreamListener

from tars.twitter.credentials.authenticate import Authenticate
from tars.twitter.tweet.interface import TweetInterface
from tars.db.insert import Insert
from tars.db.utils import get_db_engine

from sqlalchemy.exc import IntegrityError


logging.basicConfig(
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO,
    filename='/montebello/twitter/log.txt',
    filemode='a'
)
DATA_DIR = '/montebello/twitter'


class FollowListener(StreamListener):

    def is_from_creator(self, status):
        if hasattr(status, 'retweeted_status'):
            return False
        elif status.in_reply_to_status_id != None:
            return False
        elif status.in_reply_to_screen_name != None:
            return False
        elif status.in_reply_to_user_id != None:
            return False
        else:
            return True

    def on_status(self, status):
        if self.is_from_creator(status):
            id = status.id_str
            user = status.user.screen_name
            user_id = status.user.id_str
            tweet_text = status.text
            tweet_dict = status._json

            log.info(f"user_id: {user_id} | screen_name: {user} | tweet_id: {id} | {tweet_text}")

            json_fp = os.path.join(DATA_DIR, user_id, f"tweets/{id}.json")
            Path(os.path.dirname(json_fp)).mkdir(
                parents=True,
                exist_ok=True
            )

            with open(json_fp, 'w') as f:
                json.dump(tweet_dict, f, indent=4)

            tweet = TweetInterface(tweet_dict)
            try:
                Insert(database="twitter", table="tweets_log").load(data=tweet.facts)
            except IntegrityError as e:
                log.error(e)

            quoted_tweet_dict = tweet_dict.get('quoted_status', None)
            if quoted_tweet_dict:
                quoted_tweet = TweetInterface(quoted_tweet_dict)
                try:
                    Insert(database="twitter", table="quoted_tweets_log").load(data=quoted_tweet.facts)
                except IntegrityError as e:
                    log.error(e)

        return True

    def on_error(self, status):
        log.error(status)


if __name__ == '__main__':

    db_engine = get_db_engine(database="twitter")

    sql_string = "SELECT id_str FROM twitter.users_dim"
    users = [user[0] for user in db_engine.execute(sql_string).fetchall()]

    stream = Stream(
        Authenticate().get_oauth_handler(), 
        FollowListener()
    )
    stream.filter(follow=users)
