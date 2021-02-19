import pickle
import regex as re
import pandas as pd
from tqdm import tqdm


def clean_tweet(tweet)->str:
    '''
    Removes links and special characters from tweet text
    '''
    
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

def save_data(data: dict,topic='temp'):

    '''|  Saves data from tree in pickle file\n
       Parameters:\n
       |  tree_data: treelib object with twitter data\n
       |   topic: keyword used to search for tweets
    '''

    with open(f'C:/Users/anike/Desktop/code/twitter_sent/{topic}.pickle','wb') as f:
        pickle.dump(data,f)
        f.close()

def load_data(file_name)->dict:
    '''
    |  loads pickle file\n
    Parameters:\n
    |  file_name: pass a string with the files name
    '''
    path = f'C:/Users/anike/Desktop/code/twitter_sent/{file_name}'
    with open(path,'rb') as f:
        data = pickle.load(f)
        return data

def add_tree_node(tree,tweet,parent=None):
    '''
    Adds a tree node to the treelib Tree object with selected twitter object data\n
    '''
    data = {'timestamp':tweet.created_at, 'text':clean_tweet(tweet.full_text), 'likes':tweet.favorite_count, 'retweets':tweet.retweet_count}
    tree.create_node(tweet.id, tweet.id, parent=parent, data=data)

def get_dataframe(tree):
    '''
    Adds all tweet data to a dataframe from a tree and returns it
    '''

    #init dataframe
    tweet_df = pd.DataFrame(columns=['timestamp','text','likes','retweets','sentiment'])
    
    #add all tweet data to dataframe
    for tweet in tqdm(tree.all_nodes_itr()):
        #check for NULL
        if tweet.data:
            tweet_df = tweet_df.append(tweet.data,ignore_index=True)
    tweet_df = tweet_df.sort_values('timestamp')
    tweet_df['timestamp'] = pd.to_datetime(tweet_df['timestamp'])
    tweet_df['date'] = tweet_df['timestamp'].dt.date
    tweet_df['time'] = tweet_df['timestamp'].dt.time
    return tweet_df
