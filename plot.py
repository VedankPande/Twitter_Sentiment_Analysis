import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#TODO: Fix code and add dates on x axis
def plot_df(df):
    sns.set()
    for date in set(list(df['date'])):
        x = df['timestamp'][df['date']==date]
        x_lims = pd.date_range(date,periods=25,freq='H')
        y = df['sentiment'][df['date']==date]
        plt.xticks(x_lims)
        plt.plot(x,y)
        plt.show()
