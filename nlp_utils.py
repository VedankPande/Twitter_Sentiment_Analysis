import treelib
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
    root = tree_data.get_node('tweets')
    for tweet in tree_data.children(root.identifier):
        print(tweet.data)
        for reply in tree_data.children(tweet.identifier):
            print(reply.data)











