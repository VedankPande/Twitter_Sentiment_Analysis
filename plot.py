import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import preprocessing


#TODO: Fix code and add dates on x axis
def plot_df(df):
    #preprocess data
    #min_max_scaler = preprocessing.MinMaxScaler()
    #df['sentiment'] = min_max_scaler.fit_transform(df['sentiment'])

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


if __name__ == "__main__":
    pass
