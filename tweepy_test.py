import tweepy

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
def search_tweets(keyword,length):
    try:
        tweets = tweepy.Cursor(api.search,
        q=f"\"{keyword}\" -filter:retweets",
        lang='en',
        tweet_mode = 'extended'
        ).items(length)
    except Exception as e:
        print(e)

    tweets_list = [tweet.full_text for tweet in tweets]
    print(tweets_list)

#search for a particular users tweets
def search_user_status(user_name,num_tweets):
    tweets = api.user_timeline(screen_name = user_name, count = num_tweets)
    for tweet in tweets:
        print(tweet.text)

search_user_status('ManUtd', 10)




