import tweepy
import time
from treelib import Tree
from data_utils import clean_tweet,add_tree_node

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
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#stream real time tweets with filter
def stream_tweets(keyword):
    myStreamListener = StreamerListener()
    myStream = tweepy.Stream(auth = api.auth,listener=myStreamListener)
    myStream.filter(track=[keyword])        
        
#search past tweets with keywords
def search_tweets(keyword,res_type='popular',lang='en',length=10):
    try:
        # search tweets with params    
        tweets = tweepy.Cursor(api.search,
        q=f"\"{keyword}\" -filter:retweets",
        result_type =res_type,
        lang=lang,
        tweet_mode = 'extended'
        ).items(length)
    except Exception as e:
        print(e)
    #return tweet cursor
    return tweets

#search for a particular users tweets
def search_user_status(user_name,num_tweets=1):
    #return tweet cursor for user timeline
    return api.user_timeline(screen_name = user_name, count = num_tweets,tweet_mode="extended",lang='en')
    

# get replies for tweet from a specific user timeline, may take a while due to rate limiting
def get_user_tweet_replies(tweet_cursor,num_replies=100):
    tree = Tree()
    tree.create_node("Tweets","tweets")

    #use max_tweet to limit the search 
    max_tweet = None

    for tweet in tweet_cursor:
        
        add_tree_node(tree,tweet,parent='tweets')
        #get @ of target Twitter account
        target_user = '@'+tweet.user.screen_name
        tweet_id = tweet.id
        replies = tweepy.Cursor(api.search,q='to:{}'.format(target_user),
                                result_type='recent',since_id= tweet_id,
                                max_id=max_tweet,tweet_mode="extended",lang='en').items(num_replies)

        while True:
            try:
                #search for replies to given tweet
                reply = replies.next()

                #check if tweet is a reply
                if not hasattr(reply, 'in_reply_to_status_id'):
                    continue
                #check if tweet is in reply to our original tweet
                if reply.in_reply_to_status_id == tweet_id:
                    add_tree_node(tree,reply,parent=tweet_id)

            except tweepy.RateLimitError as e:
                print("Twitter api rate limit reached {}".format(e))
                time.sleep(60)
                continue

            except tweepy.TweepError as e:
                print("Tweepy error occured:{}".format(e))
                print("sleeping for 60 seconds")
                time.sleep(60)
                continue

            except StopIteration:
                print("iteration stopped")
                break

            except Exception as e:
                print("Failed while fetching replies {}".format(e))
                break
        
        #limit search space for tweets between last and current tweet
        max_tweet = tweet.id
    return tree
