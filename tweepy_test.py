import tweepy
import time
from treelib import Tree
from data_utils import add_tree_node

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

# api object
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#stream real time tweets with filter
def stream_tweets(keyword):
    myStreamListener = StreamerListener()
    myStream = tweepy.Stream(auth = api.auth,listener=myStreamListener)
    myStream.filter(track=[keyword])

#return search result for a query
def search(keyword):
    return api.search_users(keyword,count=5)  
        
# search past tweets with keywords
def search_tweets(keyword,res_type='recent',lang='en',length=10)->Tree:
    '''
    |  Returns tree with tweet data based on input keyword\n
    Parameters:\n
    |  keyword: search query for twitter search\n
    |  res_type: refer to twepy docs for options\n
    |  lang: tweet language\n
    | length: number of tweets to return\n
    '''

    #init tree
    tree = Tree()
    tree.create_node("Tweets","tweets")

    try:
        # search tweets with params    
        tweets = tweepy.Cursor(api.search,
        q=f"\"{keyword}\" -filter:retweets",
        result_type =res_type,
        lang=lang,
        tweet_mode = 'extended'
        ).items(length)
        
        #add tweets to tree
        for tweet in tweets:
            add_tree_node(tree,tweet,parent='tweets')
        
    except Exception as e:
        print(e)
    #return tweet cursor
    return tree

#search for a particular users tweets
def search_user_status(user_name,num_tweets=10):
    
    #return tweet cursor for user timeline
    try:
        return api.user_timeline(screen_name = user_name, count = num_tweets,tweet_mode="extended",lang='en')

    except tweepy.TweepError as e:
        print("Did you mean:\n")
        for user in search(user_name):
            print(f"{user.screen_name}\n or \n")
                    
    

# get replies for tweet from a specific user timeline, may take a while due to rate limiting
def get_user_tweet_replies(tweet_cursor,num_replies=100)->Tree:
    '''
    |  Returns a treelib object with tweets, their respective replies and event data (likes and retweets)\n
    |  May take a while to execute if the Twitter API rate limit is reached\n
    '''

    #init tree
    tree = Tree()
    tree.create_node("Tweets","tweets")

    #use max_tweet to limit the search 
    max_tweet = None

    # iterate through fetched tweets
    for tweet in tweet_cursor:
        
        add_tree_node(tree,tweet,parent='tweets')

        #get @ of target Twitter account
        target_user = '@'+tweet.user.screen_name
        
        #id for the root tweet (used to find replies to the root tweet)
        tweet_id = tweet.id
        replies = tweepy.Cursor(api.search,q='to:{}'.format(target_user),
                                result_type='recent',since_id= tweet_id,
                                max_id=max_tweet,tweet_mode="extended",lang='en').items(num_replies)

        while True:
            try:
                #search for replies to given tweet
                reply = replies.next()

                #check if tweet is a reply
                if not hasattr(reply,'in_reply_to_status_id'):
                    continue

                #check if tweet is in reply to our original tweet
                if reply.in_reply_to_status_id == tweet_id:
                    add_tree_node(tree,reply,parent=tweet_id)

            #handling various exceptions
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

if __name__ == "__main__":
    pass
