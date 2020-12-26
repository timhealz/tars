from __future__ import absolute_import, print_function
import logging as log

import json
import os
from pathlib import Path
from typing import List

from tweepy import API, Cursor
from sqlalchemy.exc import IntegrityError

from tars.twitter.tweet.interface import TweetInterface
from tars.db.insert import Insert
from tars.twitter.credentials.authenticate import Authenticate
from tars.utils import write_data_to_json


DATA_DIR = "/montebello/twitter"

log.basicConfig(
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.INFO,
    #filename=os.path.join(DATA_DIR, "batch_processor.log"),
    #filemode='a'
)


class BatchProcessor():
    def __init__(self):
        self.api = API(Authenticate().get_oauth_handler(), wait_on_rate_limit=True)

    def get_list_member_data(self, list_id: str) -> List:
        members = []
        for member in Cursor(self.api.list_members, list_id=list_id).items():

            id = member.id_str
            user = member.screen_name

            json_fp = os.path.join(DATA_DIR, id, "user_metadata.json")
            Path(os.path.dirname(json_fp)).mkdir(
                parents=True,
                exist_ok=True
            )

            member.__setattr__('_json_filepath', json_fp)
            members.append(member)

            with open(json_fp, 'w') as f:
                json.dump(member._json, f, indent=4)
            log.info(
                f"id: {id} | screen_name: {user} | filepath: {json_fp}")

        return members
    
    def get_tweets_from_user(self, user_id:int, n:int, min_tweet_id:int) -> List:

        tweet_cursor = Cursor(self.api.user_timeline,
            user_id=user_id,
            max_id=min_tweet_id
        )
        
        for tweet in tweet_cursor.items(n):
            user_id = tweet.user.id_str
            tweet_id = tweet.id_str
            json_fp = os.path.join(DATA_DIR, user_id, 'tweets', f'{tweet_id}.json')
            
            log.info(
                f"user id: {user_id} | tweet id: {tweet_id} | text: {tweet.text} | filepath: {json_fp}")
            write_data_to_json(tweet._json, json_fp)

            tweet_dict = tweet._json
            tweet = TweetInterface(tweet_dict)

            try:
                Insert(database="twitter", table="tweets_log").load(data=tweet.facts)
            except IntegrityError as e:
                log.warning(e._sql_message)

            reweet_dict = tweet_dict.get('retweet_status', None)
            if reweet_dict:
                retweet = TweetInterface(reweet_dict)

                try:
                    Insert(database="twitter", table="retweets_log").load(data=retweet.facts)
                except IntegrityError as e:
                    log.warning(e._sql_message)

            quoted_tweet_dict = tweet_dict.get('quoted_status', None)
            if quoted_tweet_dict:
                quoted_tweet = TweetInterface(quoted_tweet_dict)

                try:
                    Insert(database="twitter", table="quoted_tweets_log").load(data=quoted_tweet.facts)
                except IntegrityError as e:
                    log.warning(e._sql_message)

