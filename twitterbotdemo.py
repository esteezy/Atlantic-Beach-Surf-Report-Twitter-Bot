# Evan Mason
# May 9, 2020

# twitter bot using Tweepy API services
# updates on local surf info bc I hate paying for surfline
# swellinfo is old and surfline cams arent up and this is more fun

import tweepy

#defines
CONSUMER_KEY = '*******'
CONSUMER_SECRET = '*******'
ACCESS_KEY = '*******'
ACCESS_SECRET = '*******'

auth = tweepy.OAuthHandler( CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token( ACCESS_KEY, ACCESS_SECRET )
api = tweepy.API(auth)
api.retry_count = 1
api.retry_delay = 2

def postTweet(tweet):
    try:
        api.update_status(tweet)
    except tweepy.TweepError as err:
        raise UserWarning(err)

    return

