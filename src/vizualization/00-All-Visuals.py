"""
This is primarily for my own reference. It is based off notes I wrote during a
seaborn tutorial. I refer to this for the main arguments since I always get
confused while making data viz.
"""

import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Sample imports
IMPORT = "/Users/lucaspenido/Desktop/bank-data/data/processed"
os.chdir(IMPORT)
file = "STNAMEBR-Prop-Branches.csv"
index = file.split("-")[0]
df = pd.read_csv(file, index_col=index)

pd.options.display.float_format = '{:,.0f}'.format

def box_plot(df):
    sns.boxplot(data=df, showfliers=True)
    plt.title('Distributions of Bank Deposits in the US (2009-2019)')
    # plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Bank Deposits (in Billions)')
    plt.xlabel('Year')
    plt.show()

def violin_plot(df):
    """
    Seaborn takes columns, remember the columns. You can also set styles and use
    custom color palettes by making a list of hex codes.
    """
    sns.violinplot(data=df)

    plt.title('Distributions of Bank Deposits in the US (2009-2019)')
    # plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Bank Deposits (in Billions)')
    plt.xlabel('Year')

    plt.show()

def heat_map(df):
    sns.heatmap(df, annot=True, cmap="Greens", annot_kws={"fontsize":6})

    plt.title('Yearly Percent Change in Bank Branches')
    plt.ylabel('State')
    plt.yticks(rotation=0)
    sns.set(font_scale=0.8)

    plt.show()

def scatter_plot(df):
    '''
    Needs two columns.

    County data would open up more interesting plots. Some ideas:
        (Variance, 10-Year State Prop. Mean), color by rural
        ()

    10-yr deposits v. 10-yr branches
    '''
    sns.lmplot(x=df.col1, y=df.col2, data=df,
               fit_reg=False # No regression line
               ) # hue by rural

    plt.show()
