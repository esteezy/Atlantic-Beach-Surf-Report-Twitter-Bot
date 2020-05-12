# Evan Mason
# May 9, 2020

# twitter bot using Tweepy API services
# updates on local surf info bc I hate paying for surfline
# swellinfo is old and surfline cams arent up and this is more fun

import tweepy

#defines
CONSUMER_KEY = 'EL7ZXhqvAtC10hhhYmWeDXCQg'
CONSUMER_SECRET = '6Uw0G8U9PbPoT2f4mXeUOiu8uP6ORb60msl6WJmOfploKPJttO'
ACCESS_KEY = '1259306944390729728-y00FwUBrNYOBBJ1UVUY2pDx8JNZHAf'
ACCESS_SECRET = 'DFwEYAcRUxAhdlvYw88bFdATgWMXqaBcvZpqueIaPGjjK'

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

