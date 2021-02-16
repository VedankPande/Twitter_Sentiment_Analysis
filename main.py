import treelib
import argparse

from tweepy_test import search_user_status,get_user_tweet_replies
from nlp_utils import analyze_data
from data_utils import save_data,load_data


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Twitter Sentiment analysis using the Twitter API')
    parser.add_argument('keyword',type=str,
                        help='keyword used to query the twitter search-enter either a valid twitter handle of keyword(s)')
    parser.add_argument('--num_tweets',type=int,
                        help='number of tweets to return',default=100)
                                                                    
    arguments = parser.parse_args()

    cursor = search_user_status(arguments.keyword,arguments.num_tweets)
    for tweet in cursor:
        print(tweet.full_text)

