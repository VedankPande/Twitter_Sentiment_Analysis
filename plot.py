import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import preprocessing
from wordcloud import WordCloud,STOPWORDS

#TODO: Fix code and add dates on x axis
def plot_df(df):
    #preprocess data
    

    #init plot
    fig,ax = plt.subplots()

    #declare data and annotations
    x = df['timestamp']
    y = df['sentiment']
    annotations = df['user']
    ax.scatter(x,y)

    #add annotations
    for i,annot in enumerate(annotations):
        ax.annotate(annot,(x[i],y[i]))
    
    #display plot
    plt.show()

def plot_wordcloud(stopwords = STOPWORDS):
    wordcloud = WordCloud(width = 800,height = 400, background_color='salmon', relative_scaling=1.0,stopwords=stopwords).generate(' ')

    fig = plt.figure(1, figsize=(8, 4))
    plt.axis('off')
    plt.imshow(wordcloud)
    plt.axis("off")

    plt.show()



if __name__ == "__main__":
    plot_wordcloud()
