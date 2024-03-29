import argparse

from tweepy_test import search_user_status,get_user_tweet_replies,search
from nlp_utils import analyze_data
from data_utils import save_data,load_data, get_dataframe, normalize_sentiment
from plot import plot_df
import treelib

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  


if __name__ == '__main__':

    # argument parser
    parser = argparse.ArgumentParser(description='Twitter Sentiment analysis')

    #keyword argument for tweet search
    parser.add_argument('--keyword',type=str,
                        help='keyword used to query the twitter search-enter either a valid twitter handle of keyword(s)')
    # number of tweets to search/retrieve, default = 10
    parser.add_argument('--num_tweets',type=int,
                        help='number of tweets to return',default=10)

    #get arguments in a parser object                                   
    arguments = parser.parse_args()

    # Driver code
    #retrieve and save new data

    #cursor = search_user_status(arguments.keyword,arguments.num_tweets)
    #tree = get_user_tweet_replies(cursor)
    #tree = analyze_data(tree)
    #save_data(tree,"manutd")

    #load data (during dev)
    tree = load_data("manutd.pickle")

    #convert tree to dataframe
    df = get_dataframe(tree)

    #normalize sentiment column
    df = normalize_sentiment(df)
    
    #plot dataframe
    plot_df(df)


