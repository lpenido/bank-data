"""
Loops through each year of FDIC data (2009-2019)to get a standardized flexible
table to work with for the 10-year data.

Base Table Variables:
STCNTYBR = County codes for each branch, known as FIPS codes
STNAMEBR = Names of the State the branch is located in
DEPSUMBR = Sum of the deposits located within the branch
NAMEBR = Name of the bank branch
YEAR = Year from which the data was gathered
"""
import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join

IMPORT = "/Users/lucaspenido/Desktop/bank-data/data/raw"
EXPORT = "/Users/lucaspenido/Desktop/bank-data/data/interim"
os.chdir(IMPORT)

def get_base_table():
    '''
    Gets the FIPS codes, State Names, Branch Names, and Branch Deposits for all
    51 areas over 10 years.

    At some point move vars up to the kwargs section to allow for slinging new
    base_tables out easy
    '''

    vars = ['STCNTYBR','STNAMEBR','DEPSUMBR','NAMEBR','YEAR']
    filelist = [f for f in listdir(IMPORT) if isfile(join(IMPORT, f))]

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
    os.chdir(EXPORT)
    base_table.to_csv("00-Base-Table.csv", index=False)
get_base_table()
