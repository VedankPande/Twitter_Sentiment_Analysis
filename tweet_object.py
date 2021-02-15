import tweepy 
from sys import getsizeof
class TweetClass:
    def __init__(self,text,likes,retweets):
        self.text = text
        self.likes = likes
        self.retweets = retweets
    
    def __add__(self,other):
        return {'likes':self.likes+other.likes,'retweets':self.retweets+other.retweets}


if __name__ == "__main__":
    a = TweetClass("hello asdfjasdokf ja sijfa[sdofj adsofjasdkf asdkaskfna sdfasdhfasodnfalsdjfoa #MUNLIV",20,100)
    b = TweetClass("world",25,100)
    c = {'text':"hello asdfjasdokf ja sijfa[sdofj adsofjasdkf asdkaskfna sdfasdhfasodnfalsdjfoa #MUNLIV",'likes':20,'retweets':100}

    print(getsizeof(a),getsizeof(b),getsizeof(c))