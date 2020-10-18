# Importing libraries:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Importing the os library specifically for reading the csv once I've created the file in my working directory.
import os

# libraries needed for preparing the data:
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler
# from sklearn.preprocessing import MinMaxScaler
import sklearn.preprocessing

# Setting up the user credentials:

from env import host, user, password

# The 
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}' 


# acquiring mall_customer database:
def get_mall_data():
    sql_query = '''
            SELECT *
            FROM customers
            '''

    df = pd.read_sql(sql_query, get_connection('mall_customers'))
    return df


# Prepping the mall data:

def split_mall_data(df):
    # df = get_mall_data()
    # Splitting my data based on the target variable of tenure:
    train_validate, test = train_test_split(df, test_size=.15, random_state=123, stratify = df.gender)
    
    # Splitting the train_validate set into the separate train and validate datasets.
    train, validate = train_test_split(train_validate, test_size=.20, random_state=123, stratify = train_validate.gender)
    
    # Printing the shape of each dataframe:
    print(f'Shape of train df: {train.shape}')
    print(f'Shape of validate df: {validate.shape}')
    print(f'Shape of test df: {test.shape}')
    return train, validate, test


# Finding outliers by IQR:
def get_upper_outliers(s, k):
    '''
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.

    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    '''
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

def add_upper_outlier_columns(df, k):
    '''
    Add a column with the suffix _outliers for all the numeric columns
    in the given dataframe.
    '''
    # outlier_cols = {col + '_outliers': get_upper_outliers(df[col], k)
    #                 for col in df.select_dtypes('number')}
    # return df.assign(**outlier_cols)

    for col in df.select_dtypes('number'):
        df[col + '_outliers'] = get_upper_outliers(df[col], k)

    return df

print("file loaded successfully")