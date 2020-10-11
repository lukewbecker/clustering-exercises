# Creating the aquire.py file

# Make a new python module, acquire.py to hold the following data aquisition functions:
# get_titanic_data
# get_iris_data

# Importing libraries:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Importing the os library specifically for reading the csv once I've created the file in my working directory.
import os

# Make a function named get_titanic_data that returns the titanic data from the codeup data science database as a pandas data frame. Obtain your data from the Codeup Data Science Database.

# Setting up the user credentials:

from env import host, user, password

def get_db(db, user=user, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# Telco acquire function
# Being explicit in my SQL query allows me to only pull the extra info from the columns in the other tabes that I actually need, instead of returning the repeated foreign key columns. Saves me time on the prepare step.
# This acquire function will allow the user, with proper credentials to the CodeUp database access the same original dataframe that I started with in my process.
# It will first search for a csv file containing the appropriate telco data in the same folder that the jupyter notebook is being run in, and if it doesn't find one
# the function will execute the MySQL query call and create a local copy of the telco dataset.

# Recall, the way to call this function specifically is to type the following:
#   from acquire.py import get_telco_data
# That'll import this function for use in your own notebook.

def get_zillow_data():

    '''
    This function will allow the user to retrieve all tables from the Zillow database from the Codeup DB source. 
    It will acquire the data, import it as a dataframe, and then write that dataframe to a .csv file in the local directory.
    '''

    zillow_sql_query = '''
                SELECT * 
                    FROM properties_2017
                    JOIN (select id, logerror, pid, tdate FROM predictions_2017 pred_2017
                    JOIN (SELECT parcelid AS pid, Max(transactiondate) as tdate FROM predictions_2017 GROUP BY parcelid) AS sq1
                    ON (pred_2017.parcelid = sq1.pid AND pred_2017.transactiondate = sq1.tdate)) AS sq2
                    ON (properties_2017.parcelid = sq2.pid)
                    LEFT JOIN airconditioningtype USING (airconditioningtypeid)
                    LEFT JOIN architecturalstyletype USING (architecturalstyletypeid)
                    LEFT JOIN buildingclasstype USING (buildingclasstypeid)
                    LEFT JOIN heatingorsystemtype USING (heatingorsystemtypeid)
                    LEFT JOIN propertylandusetype USING (propertylandusetypeid)
                    LEFT JOIN storytype USING (storytypeid)
                    LEFT JOIN typeconstructiontype USING (typeconstructiontypeid)
                    LEFT JOIN unique_properties USING (parcelid)
                    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
                '''
    
    
    filename = 'zillow_clustering_data.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        zillow_df = pd.read_sql(zillow_sql_query, get_db('zillow'))
        zillow_df.to_csv(filename, index = False)
        
    return zillow_df


print('End of file.')