import pickle
import regex as re

def clean_tweet(tweet)->'String':
    '''
    Removes links and special characters from tweet text
    '''
    
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

def save_data(data: dict,topic='temp'):
    '''saves data from tree in pickle file
        tree_data: treelib object with twitter data
        topic: keyword used to search for tweets'''

    with open(f'C:/Users/anike/Desktop/code/twitter_sent/{topic}.pickle','wb') as f:
        pickle.dump(data,f)
        f.close()

def load_data(file_name)->dict:
    '''
    loads pickle file
    file_name: pass a string with the files name
    '''
    path = f'C:/Users/anike/Desktop/code/twitter_sent/{file_name}'
    with open(path,'rb') as f:
        data = pickle.load(f)
        return data

