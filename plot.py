import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#TODO: Fix code and add dates on x axis
def plot_df(df):
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
