"""
3. Vizualize State level change using heatmap of change across state and year change

Heatmaps look cool, but I'd like to filter out outliers since South Dakota kinda
obscures other trends.

"""
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

general  = "/Users/lucaspenido/Desktop/bank-data"
base_table = 'base_table.csv'
state_deps = 'STNAMEBR_deposits.csv'
state_prop_deps = 'STNAMEBR_prop_deposits.csv'
state_prop_bran = 'STNAMEBR_prop_branches.csv'

pd.options.display.float_format = '{:,.0f}'.format

def load_save(path,file):

    os.chdir(path)
    df = pd.read_csv(file, encoding='utf-8')

    df.reset_index(inplace=True)
    df.STNAMEBR = df.STNAMEBR.astype(str)
    df.set_index('STNAMEBR',inplace=True)
    df.drop(['index'], axis=1, inplace=True)

    print(df.dtypes)
    print(df.head())

    return df
df = load_save(general,state_prop_bran)

# df.loc['South Dakota', '2011'] = 70
# print(df.loc['South Dakota', '2011'])

def box_plot(df):
    sns.boxplot(data=df, showfliers=True)
    plt.title('Distributions of Bank Deposits in the US (2009-2019)')
    # plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Bank Deposits (in Billions)')
    plt.xlabel('Year')
    plt.show()
# box_plot(df)

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
# violin_plot(df)

def heat_map(df):
    sns.heatmap(df, annot=True, annot_kws={"fontsize":6})

    plt.title('Yearly Percent Change in Bank Branches')
    plt.ylabel('State')
    plt.yticks(rotation=0)
    sns.set(font_scale=0.8)

    plt.show()
heat_map(df)

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
# scatter_plot(df)
