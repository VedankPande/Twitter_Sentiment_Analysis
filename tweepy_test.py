import tweepy

API_KEY = #enter you key/token here
API_SECRET_KEY = #enter you key/token here
ACCESS_TOKEN = #enter you key/token here
ACCESS_TOKEN_SECRET = #enter you key/token here

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
def search_tweets(keyword,length):
    try:
        tweets = tweepy.Cursor(api.search,
        q='\"Rashford is best\" -filter:retweets',
        lang='en',
        tweet_mode = 'extended'
        ).items(length)
    except Exception as e:
        print(e)

    tweets_list = [tweet.full_text for tweet in tweets]
    print(tweets_list)
