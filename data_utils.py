import pickle
import regex as re
import treelib

#TODO: add clean tweet code
def clean_tweet(tweet)->object:
    '''Removes links and special characters from tweet text'''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

#TODO: add pickle save code
def save_data(tree_data : ,topic='temp'):
    '''saves data from tree in pickle file
        tree_data: treelib object with twitter data
        topic: keyword used to search for tweets'''

    data = tree_data.to_dict(with_data=True)
    with open(f'C:/Users/anike/Desktop/code/{topic}','wb') as f:
        pickle.dump(data,f)
        f.close()

def load_data(path = 'C:/Users/anike/Desktop/code/data.txt')->dict:
    with open(path,'rb') as f:
        data = pickle.load(f)
        return data