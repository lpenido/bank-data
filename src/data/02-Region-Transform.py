"""
These functions return summary statistics for each of the Region Tables created
in 01-Region-Tables.

Proportional change will return a df
10-year variance will return a single number
Change per 1000 will take some more time, needs an external merge for population
"""
import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

IMPORT = "/Users/lucaspenido/Desktop/bank-data/data/interim/01-Region-Tables"
EXPORT = "/Users/lucaspenido/Desktop/bank-data/data/interim/02-Region-Transform"

pd.options.display.float_format = '{:,.0f}'.format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Helper functions to be applied later
def proportional_change(df, filename, write):
    """
    Given df = {rows:regions, cols:years}, loop over every column and apply a
    function to it.
    """
    # Empty df to populate
    change = pd.DataFrame()

    # Getting proportional change, ( (i+1)-(i) )/ (i) * 100
    df.columns = df.columns.astype(int)
    cols = list(df.columns.values)
    for i in cols:
        next = i+1
        if i != cols[-1]:
            print("Subtracting " + str(next) + " from " + str(i))
            proportion = ((df[next] - df[i]) / df[i]) * 100
            change[next] = proportion

    if write:
        print("Writing to csv")
        os.chdir(EXPORT)
        filename = "02-" + filename + "-PropChange.csv"
        change.to_csv(filename, index=True)
    else:
        print(change.shape)
        return change

def get_variance(df, write):
    """
    Get variance of columns (within years) and rows (across years).
    """
    change = pd.DataFrame()
    df.set_index(["STNAMEBR"], inplace=True)

    # Type setting
    for col in df.columns:
        df[col] = df[col].astype(float)

    # Ordering columns for iteration
    cols = list(df.columns.values)
    cols.sort()
    df = df[cols]

    # Getting national proportional change
    for i in cols:
        sample = list(df[i].values)
        # print("The Proportion of Branch Change for", i, np.var(sample))

    # Getting 10-yr variance
    row_list = []
    for i in cols:
        for index, rows in df.iterrows():
            print(i, index, rows)
            my_list = rows[i]
            row_list.append(my_list)

    # # Create an empty list
    # Row_list =[]
    #
    # # Iterate over each row
    # for index, rows in df.iterrows():
    #     # Create list for the current row
    #     my_list =[rows.Date, rows.Event, rows.Cost]
    #
    #     # append the list to the final list
    #     Row_list.append(my_list)

    # Print the list
    # print(row_list)

    if write:
        print("Writing to csv")
        os.chdir(EXPORT)

        change.to_csv("STNAMEBR_prop_deposits.csv", index=True)
    else:
        return change
# get_variance(branches, write=False)

# One loop to write them all...
os.chdir(IMPORT)
filelist = [f for f in listdir(IMPORT) if isfile(join(IMPORT, f))]
for file in filelist:
    index = file.split("-")[1]
    filename = file[3:20]
    df = pd.read_csv(file, index_col=index, encoding="latin")
    proportional_change(df, filename, True)
    os.chdir(IMPORT)
