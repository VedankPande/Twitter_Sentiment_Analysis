import tweepy
import logging
import time
import pandas as pd
from treelib import Node,Tree

API_KEY = 
API_SECRET_KEY = 
ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET = 

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
    tweets = api.user_timeline(screen_name = user_name, count = num_tweets)
    return tweets


# Function to update a df with new data
#TODO: change code according to new GET function
def update_df(data_frame,keyword,num=10):

    tweets_list = search_tweets(keyword,length=num)
    table = [[tweet.id,
            tweet.user.screen_name,
            tweet.full_text,tweet.favorite_count,
            tweet.retweet_count] for tweet in tweets_list]
    data_frame  = data_frame.append(pd.DataFrame(data=table,columns=['id','user','status','likes','rt']))
    return data_frame
    

# get replies for tweet from a specific user timeline, may take a while due to rate limiting
def get_user_tweet_replies(tweet_cursor):
    tree = Tree()
    tree.create_node("Tweets","tweets")

    #use max_tweet to limit the search 
    max_tweet = None

    for tweet in tweet_cursor:

        tree.create_node(tweet.id,tweet.id,parent="tweets",data=tweet.text)
        target_user = '@'+tweet.user.screen_name
        test_tweet_id = tweet.id
        replies = tweepy.Cursor(api.search,q='to:{}'.format(target_user),
                                result_type='recent',since_id=test_tweet_id,
                                max_id=max_tweet).items(100)

        while True:
            try:
                #search for replies to given tweet
                reply = replies.next()
                if not hasattr(reply, 'in_reply_to_status_id'):
                    continue
                if reply.in_reply_to_status_id == test_tweet_id:
                    tree.create_node(reply.user.screen_name,reply.id,parent=test_tweet_id,data=reply.text)

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

tweets = search_user_status('OfficialFPL',13)
tree = get_user_tweet_replies(tweets)
print(tree,type(tree))