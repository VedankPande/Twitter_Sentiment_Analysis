import tweepy
import logging
import time
import pandas as pd

API_KEY = '4EWB8qGkqRfMsnuF9wAIF1OE1'
API_SECRET_KEY = 'S3EMY5ETmxiUtUYr2g1ynbdGvRisSIuCdeJK1Gr0AbevQACcjb'
ACCESS_TOKEN = '896024023531913217-TyclTbVKs6ZEPL3gRQeQ1cbKdtvighM'
ACCESS_TOKEN_SECRET = 'oNVVcEt7015skXLQwpgjajcEujZieIsSnvRizFSx2QQko'

#class for tweepy StreamerListener
class StreamerListener(tweepy.StreamListener):

    def on_status(self,status):
        print(status.text)

    def on_error(self,status_code):
        if status_code==420:
            return False
    

# authentication
auth = tweepy.OAuthHandler(API_KEY,API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

#api object
api = tweepy.API(auth)

#stream real time tweets with filter
def stream_tweets(keyword):
    myStreamListener = StreamerListener()
    myStream = tweepy.Stream(auth = api.auth,listener=myStreamListener)
    myStream.filter(track=[keyword])        
        
#search past tweets with keywords
def search_tweets(keyword,res_type='popular',lang='en',length=10):
    try:
        tweets = tweepy.Cursor(api.search,
        q=f"\"{keyword}\" -filter:retweets",
        result_type =res_type,
        lang=lang,
        tweet_mode = 'extended'
        ).items(length)
    except Exception as e:
        print(e)
    return tweets

df = pd.DataFrame(columns=['id','user','status','likes','rt'])

#search for a particular users tweets
def search_user_status(user_name,num_tweets):
    tweets = api.user_timeline(screen_name = user_name, count = num_tweets)
    return tweets


# Function to update a df with new data
#TODO: change code according to new GET function
def update_df(data_frame,keyword,num=10):

    tweets_list = search_tweets(keyword,length=num)
    table = [[tweet.id,tweet.user.screen_name,tweet.full_text,tweet.favorite_count,tweet.retweet_count] for tweet in tweets_list]
    data_frame  = data_frame.append(pd.DataFrame(data=table,columns=['id','user','status','likes','rt']))
    return data_frame
    

# get replies for tweet, may take a while due to rate limiting
def get_replies(tweet_cursor):
    for tweet in tweet_cursor:
        target_user = '@'+tweet.user.screen_name
        test_tweet_id = tweet.id
        print(f"target user: {target_user}, tweet_id: {test_tweet_id}")
        replies = tweepy.Cursor(api.search,q='to:{}'.format(target_user),since_id=test_tweet_id).items()
        while True:
            try:
                reply = replies.next()
                if not hasattr(reply, 'in_reply_to_status_id_str'):
                    continue
                if reply.in_reply_to_status_id == test_tweet_id:
                    print("reply of tweet:{}".format(reply.text))

            except tweepy.RateLimitError as e:
                print("Twitter api rate limit reached {}".format(e))
                time.sleep(60)
                continue

            except tweepy.TweepError as e:
                print("Tweepy error occured:{}".format(e))
                break

            except StopIteration:
                print("iteration stopped")
                break

            except Exception as e:
                print("Failed while fetching replies {}".format(e))
                break
