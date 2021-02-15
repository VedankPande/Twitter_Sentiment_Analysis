import treelib
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm import tqdm
from math import copysign

nltk.download('vader_lexicon')

def get_sentiment_dict(text)->dict:
    
    sent_analyzer = SentimentIntensityAnalyzer()
    sent_dict = sent_analyzer.polarity_scores(text)
    return sent_dict

#TODO: add NLP code for dict here
def analyze_data(tree_data):
    '''
    returns total sentiment value for the whole topic/keyword
    '''
    total_score = 0
    #root node
    root = tree_data.get_node('tweets')
    #for each node, add it's sentiment score along with the reply score's
    for tweet in tree_data.children(root.identifier):

        sent_score = get_sentiment_dict(tweet.data['text'])['compound']

        #since most people that retweet, also like the tweet, assign lower weight to retweets
        #add one to prevent 0 likes+retweets to nullify a tweet
        event_score = tweet.data['likes']+(tweet.data['retweets']*0.3)+1
        total_score += sent_score*event_score
        
        for reply in tqdm(tree_data.children(tweet.identifier)):
            
            sent_score = get_sentiment_dict(reply.data['text'])['compound']
            event_score = tweet.data['likes']+(tweet.data['retweets']*0.3)+1
            total_score += sent_score*event_score

    print(total_score)











