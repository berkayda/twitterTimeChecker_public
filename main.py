import tweepy
from datetime import datetime, timedelta, timezone
import time
import pytz

consumer_key = "WRITEYOURS"
consumer_secret = "WRITEYOURS"
access_token = "WRITE-YOURS"
access_token_secret = "WRITEYOURS"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

istanbul_timezone = pytz.timezone("Europe/Istanbul")

user = "WRITEUSERNAME"

following = []
for friend in tweepy.Cursor(api.get_friends, screen_name=user).items():
    #time.sleep(4)
    following.append(friend.screen_name)

print("FOLLOWING COUNT: " + str(len(following)))

skip_users = ["FINANCIALJUICE", "ELONMUSK"]

print("SKIP USER: " + str(len(skip_users)))

not_tweeting_users = []

for username in following:
    if username in skip_users:
        continue
    try:
        user_tweets = api.user_timeline(screen_name=username, count=3, include_rts=True, tweet_mode='extended')
        time.sleep(3)

        if len(user_tweets) > 0:
            tweet = user_tweets[0]
            tweet_time = tweet.created_at.replace(tzinfo=pytz.utc).astimezone(istanbul_timezone)
            print(username + " tweet_time: " + str(tweet_time))
            time_difference = datetime.now(istanbul_timezone) - timedelta(days=31)
            if tweet_time > time_difference:
                continue
            else:
                not_tweeting_users.append(username)
        else:
            not_tweeting_users.append(username)
            print(f"{username} did not share any tweet.")
    except tweepy.TweepyException:
        not_tweeting_users.append(username)
        print(f"{username} ERROR")

print("----------THERE IS NO TWEET IN LAST WEEK----------")
print("COUNT: " + str(len(not_tweeting_users)))
print()
for username in not_tweeting_users:
    print(username)
