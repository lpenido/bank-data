"""
2. Loop through to find yearly change for State and County

Work on getting the county/state level switch as east as possible. For the
county values, I will need to keep the State name with the FIPS codes in a
seperate column.

The County is a more general data set. I should look to make the dataset that is
most flexible. Iterating over the whole decade is not very cash money. I would need
FIPS, STATENAME, YEAR-SUMDEPS, YEAR-COUNTBRANCH. With this, I can filter and
transform as needed.
"""
import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

# DEPSUMBR for STNAMEBR, STCNTYBR
mypath  = "/Users/lucaspenido/Desktop/bank-data/deposits"
mypath2  = "/Users/lucaspenido/Desktop/bank-data"
filelist = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def get_years(list,region):

    os.chdir(mypath)

    # Create df to be merge
    to_merge = pd.DataFrame()

    for file in filelist:

        # Open .csv and format
        # Some tables are not formatted as string, not sure how to check
        df = pd.read_csv(file, encoding='latin')
        df['DEPSUMBR'] = df['DEPSUMBR'].astype(str)
        df['DEPSUMBR'] = df['DEPSUMBR'].str.replace(',','').astype(int)

        # Sum to region and label
        year = file[4:8]
        df = df.groupby([region])[['DEPSUMBR']].sum()
        df.rename(columns={'DEPSUMBR':year},inplace=True)

        # Drop territories
        df.reset_index(inplace=True)
        df.set_index(region)

        # Join to df
        if file == filelist[0]:
            to_merge = df
        else:
            to_merge = pd.merge(df,to_merge, on=region)

        print("Merging", year)
    to_merge.set_index(region, inplace=True)
    return to_merge

def get_change(df):

    change = pd.DataFrame()

    # Ordering columns for iteration
    cols = list(df.columns.values)
    cols.sort()
    df = df[cols]

    # Getting proportional change, ( (i+1)-(i) )/ (i) * 100
    for i in cols:

        # Had to make this to resolve Type Errors
        next = str(int(i)+1)

        if i != cols[-1]:
            print('Subtracting ' + next + ' from ' + i)
            proportion = ((df[next]-df[i]) / df[i]) * 100
            change[next] = proportion

    return change

def data_output(filelist,region):

    territories = ['American Samoa','Federated States Of Micronesia','Palau',
                   'Northern Mariana Islands','Marshall Islands','Guam',
                   'Virgin Islands Of The U.S.','Puerto Rico']

    merged_df = get_years(filelist,region)
    df = get_change(merged_df)

    print("To Drop")
    if region == "STNAMEBR":
        states = df.index.unique()
        for territory in territories:
            if territory in states:
                df.drop(territory, inplace=True)

    filename = region + "-PropChange.csv"
    os.chdir(mypath2)
    df.to_csv(filename, index=True)

# data_output(filelist,"STNAMEBR")
