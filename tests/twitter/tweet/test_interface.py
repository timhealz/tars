import os
import unittest

from tars.utils import read_json_to_dict
from tars.twitter.tweet.interface import TweetInterface

resources_dir = os.path.join(os.environ["HOME"], 'tarscode/tars/tests/twitter/resources')


class TestTweetInterface(unittest.TestCase):

    test_tweet = read_json_to_dict(os.path.join(resources_dir, 'tweet.json'))
    test_retweet = read_json_to_dict(os.path.join(resources_dir, 'retweet.json'))
    test_quoted_tweet = read_json_to_dict(os.path.join(resources_dir, 'quoted_tweet.json'))

    def test_init(self):
        tweet = TweetInterface(tweet_dict=self.test_tweet)
        self.assertEqual(self.test_tweet['id'], tweet.tweet_dict['id'])


if __name__ == '__main__':
    unittest.main()