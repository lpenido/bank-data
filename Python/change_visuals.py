"""
3. Vizualize State level change using heatmap of change across state and year change

Heatmaps look cool, but I'd like to filter out outliers since South Dakota kinda
obscures other trends. 

County data would open up scatterplots. I'd like a color by
"""
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

mypath  = "/Users/lucaspenido/Desktop/bank-data"

def load_save(path,region):

    os.chdir(mypath)
    df = pd.read_csv("STNAMEBR-PropChange.csv", encoding='utf-8')

    df.reset_index(inplace=True)
    df.STNAMEBR = df.STNAMEBR.astype(str)
    df.set_index('STNAMEBR',inplace=True)
    df.drop(['index'], axis=1, inplace=True)

    print(df.dtypes)
    print(df.head())

    return df
df = load_save(mypath,"STNAMEBR")

# df.loc['South Dakota', '2011'] = 70
# print(df.loc['South Dakota', '2011'])

def box_plot(df):
    sns.boxplot(data=df, showfliers=False)
    plt.show()
# box_plot(df)

def heat_map(df):
    sns.heatmap(df, annot=True, annot_kws={"fontsize":6})

    plt.title('Yearly Percent Change in Bank Deposits')
    plt.ylabel('State')
    plt.yticks(rotation=0)
    sns.set(font_scale=0.8)

    plt.show()
heat_map(df)
