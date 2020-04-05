"""
These functions create two tables with the same rows and columns, but with
different values.

"get_deposit_sum()" makes a table where the values are the deposits within the
branches in a given "region".

"get_branch_count()" makes a table where the values are the number of branches
in a given "region".

Each function takes three arguments, (df, region, write), which are as follows:

"df" (type pandas DataFrame object): this will always be the base table to be
aggregated

"region" (type string): this will always either be "STNAMEBR" or "STCNTYBR" and
determines the level of aggregation the function will perform, either by state
or by county.

"write" (type boolean): this will write the progress of the aggregation. In all
honesty I should probably delete it.
"""

import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

IMPORT = "/Users/lucaspenido/Desktop/bank-data/data/interim"
EXPORT = IMPORT + "/01-Region-Tables"
BASE_TABLE = "00-Base-Table.csv"
STATE = "STNAMEBR"
COUNTY = "STCNTYBR"

os.chdir(IMPORT)
df = pd.read_csv(BASE_TABLE, encoding="latin")

def get_deposit_sum(df, region, write):
    """
    Get a sum of deposits for any given region across all years.
    """

    # Sum Deposits and Count Branches
    df = df[[region,"DEPSUMBR","YEAR"]]
    df = df.groupby([region,"YEAR"])["DEPSUMBR"].aggregate("sum").unstack()

    if write:
        print("Writing to csv")
        os.chdir(EXPORT)
        filename = "01-"region+"-Deposits.csv"
        df.to_csv(filename, index=True)
    else:
        return df
get_deposit_sum(df, COUNTY, True)

def get_branch_count(df, region, write):
    """
    Get a sum of branches for any given region across all years.
    Make regions rows and years columns.
    """

    # Sum Deposits and Count Branches
    df = df[[region,"NAMEBR","YEAR"]]
    df = df.groupby([region,"YEAR"])["NAMEBR"].aggregate("count").unstack()

    if write:
        print("Writing to csv")
        os.chdir(EXPORT)
        filename = "01-"region+"-Branches.csv"
        df.to_csv(filename, index=True)
    else:
        return df
get_branch_count(df, STATE, True)
