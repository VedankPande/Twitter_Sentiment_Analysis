import tweepy
import time
from treelib import Node,Tree
import pickle
import regex as re
from data_utils import clean_tweet


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

#search for a particular users tweets
def search_user_status(user_name,num_tweets=1):
    return api.user_timeline(screen_name = user_name, count = num_tweets)
    

# get replies for tweet from a specific user timeline, may take a while due to rate limiting
def get_user_tweet_replies(tweet_cursor):
    tree = Tree()
    tree.create_node("Tweets","tweets")

    #use max_tweet to limit the search 
    max_tweet = None

    for tweet in tweet_cursor:
        
        tree.create_node(tweet.id_str,tweet.id,parent="tweets",data=clean_tweet(tweet.text))
        target_user = '@'+tweet.user.screen_name
        tweet_id = tweet.id
        replies = tweepy.Cursor(api.search,q='to:{}'.format(target_user),
                                result_type='recent',since_id=tweet_id,
                                max_id=max_tweet).items(100)

        while True:
            try:
                #search for replies to given tweet
                reply = replies.next()
                if not hasattr(reply, 'in_reply_to_status_id'):
                    continue
                if reply.in_reply_to_status_id == tweet_id:
                    tree.create_node(reply.user.screen_name,reply.id,parent=tweet_id,data=clean_tweet(reply.text))

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
        
            #limit search space for tweets between last and current tweet
        max_tweet = tweet.id
    return tree
