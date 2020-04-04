"""
2. Loop through to find yearly change for State and County

Would variance be between the national 10-year mean or the state's 10-year mean?
The state 10-year makes sense, but what if the state has been trending negative
at a consistent rate, then the variance would come back low. That would have to
be coupled with the direction of change.

Need a system to export data into files before the .csvs get out of control. I'm
thinking that labeling folders by the region kwarg might be helpful to organize
data export and inport into. For example, path = general + /region
"""
import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

# DEPSUMBR for STNAMEBR, STCNTYBR
# pd.options.display.float_format = '{:,.0f}'.format
pd.set_option('display.max_columns', None)

data = "/Users/lucaspenido/Desktop/bank-data/deposits"
general = "/Users/lucaspenido/Desktop/bank-data"
county = 'STCNTYBR'
state = 'STNAMEBR'

def get_base_table():
    '''
    Gets the FIPS codes, State Names, Branch Names, and Branch Deposits for all
    51 areas over 10 years.

    At some point move vars up to the kwargs section to allow for slinging new
    base_tables out easy
    '''

    os.chdir(data)
    vars = ['STCNTYBR','STNAMEBR','DEPSUMBR','NAMEBR','YEAR']
    filelist = [f for f in listdir(data) if isfile(join(data, f))]
    # list = list[0:2]
    # print(list)

    for file in filelist:

        year = file[4:8]
        print('Starting', year)

        # Open .csv and remove comma currency format
        # Some tables are formatted as object, not sure how to convert to str
        # Also had to fix DC
        df = pd.read_csv(file, encoding='latin')
        df = df[vars]
        df['DEPSUMBR'] = df['DEPSUMBR'].astype(str)
        df['DEPSUMBR'] = df['DEPSUMBR'].str.replace(',','').astype(float)

        alias = 'District Of Columbia'
        correct = 'District of Columbia'
        df['STNAMEBR'] = df['STNAMEBR'].str.replace(alias, correct)

        # Drop territories
        territories = ['American Samoa','Federated States Of Micronesia','Palau',
                       'Northern Mariana Islands','Marshall Islands','Guam',
                       'Virgin Islands Of The U.S.','Puerto Rico',
                       'Federated States of Micronesia', 'Virgin Islands of the U.S']
        for territory in territories:
            df = df[df['STNAMEBR'] != territory]

        if len(df['STNAMEBR'].unique()) > 51:
            print('Territory Error in', file)
            print(df['STNAMEBR'].unique())

        # Roll into one table
        if file == filelist[0]:
            base_table = df
        else:
            print(year,'Start:', base_table.shape[0], 'df:', df.shape[0])
            base_table = base_table.append(df)
            print('New:', base_table.shape[0])

    # Saving base table
    print("Writing to csv")
    os.chdir(general)
    base_table.to_csv("base_table.csv", index=False)
# get_base_table()

os.chdir(general)
base_table = pd.read_csv('base_table.csv', encoding='latin')
branches = pd.read_csv('STNAMEBR_prop_branches.csv', encoding='latin')

def get_deposit_sum(df,region,write):
    '''
    Get a sum of deposits for any given region across all years.
    Make df = {rows:region, cols:years}.

    1. Aggregate from county to State, without losing years
    2. Stretch out years
    '''

    # Sum Deposits and Count Branches
    df = df[[region,'DEPSUMBR','YEAR']]
    df = df.groupby([region,'YEAR'])['DEPSUMBR'].aggregate('sum').unstack()

    if write:
        print("Writing to csv")
        os.chdir(general)
        df.to_csv("STNAMEBR_deposits.csv", index=True)
    else:
        return df
# deposits = get_deposit_sum(base_table,region=state, write=False)

def get_branch_count(df,region,write):
    '''
    Get a sum of branches for any given region across all years.
    Make regions rows and years columns.
    '''

    # Sum Deposits and Count Branches
    df = df[[region,'NAMEBR','YEAR']]
    df = df.groupby([region,'YEAR'])['NAMEBR'].aggregate('count').unstack()

    if write:
        print("Writing to csv")
        os.chdir(general)
        filename = region + "-branches.csv"
        df.to_csv(filename, index=True)
    else:
        return df
# get_branch_count(base_table, state, False)

def get_proportional_change(df,write):
    '''
    Given df = {rows:regions, cols:years}, loop over every column and apply a
    function to it.

    10-year variance will return a single number
    Proportional change will return a df

    Change per 1000 will take some more time, needs FIPS merge.
    '''
    change = pd.DataFrame()

    # Type setting
    for col in df.columns:
        df[col] = df[col].astype(int)

    # Ordering columns for iteration
    cols = list(df.columns.values)
    cols.sort()
    df = df[cols]

    # Getting proportional change, ( (i+1)-(i) )/ (i) * 100
    for i in cols:

        # Had to make this to resolve Type Errors
        next = int(i)+1

        if i != cols[-1]:
            print('Subtracting ' + str(next) + ' from ' + str(i))
            proportion = ((df[next] - df[i]) / df[i]) * 100
            change[next] = proportion

    if write:
        print("Writing to csv")
        os.chdir(general)

        change.to_csv("STNAMEBR_prop_deposits.csv", index=True)
    else:
        return change
# get_proportional_change(branches, write=True)

def get_variance(df, write):

    print(df.head())
    """
    Get variance of columns (within years) and rows (across years).
    """
    change = pd.DataFrame()
    df.set_index(['STNAMEBR'], inplace=True)

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
        os.chdir(general)

        change.to_csv("STNAMEBR_prop_deposits.csv", index=True)
    else:
        return change
get_variance(branches, write=False)

print('All done!')

# data_output(filelist,"STNAMEBR")
