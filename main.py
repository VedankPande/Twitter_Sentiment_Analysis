import tweepy_test
import nlp_utils
import data_utils
import treelib

if __name__ == '__main__':
    tree =  data_utils.load_data('ManUtd.pickle')
    nlp_utils.analyze_data(tree)