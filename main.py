from tweepy_test import search_user_status,get_user_tweet_replies
from nlp_utils import analyze_data
from data_utils import save_data,load_data
from wordcloud import WordCloud,STOPWORDS
import treelib

if __name__ == '__main__':

    START_DATE = ''
    END_DATE = ''
    tree = load_data('elon.pickle')
    print(tree)
    analyze_data(load_data('elon.pickle'))