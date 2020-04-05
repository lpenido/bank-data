"""
This script takes a 02-Region-Transform table and vizualizes a heatmap from it.
So far it can only do by state (STNAMEBR) because there are too many counties to
fit on the y-axis.
"""
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

IMPORT = "/Users/lucaspenido/Desktop/bank-data/data/interim/02-Region-Transform"
file = "02-STNAMEBR-Branches-PropChange.csv"
index = file.split("-")[1]

os.chdir(IMPORT)
df = pd.read_csv(file, index_col=index)

def heat_map(df):
    sns.heatmap(df,
                cmap="YlGnBu", # Pretty colors from the default selection
                annot=True,    # Writes the data value in each cell
                annot_kws={"fontsize":6}, # Formats text in annot cells
                xticklabels=True, # Show all x-label
                yticklabels=True) # Show all y-label

    plt.title('Yearly Percent Change in Bank Branches')
    plt.ylabel('State')
    plt.yticks(rotation=0)
    sns.set(font_scale=0.8)

    plt.show()
heat_map(df)
