import requests
import pandas as pd
import numpy as np
import os
from env import get_db_url


def grab_swapi_api_df(topic):
    '''specific for swapi api, input people, planets, or starships
    
    return: df'''
    filename = (f'{topic}.csv')
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=[0])

    else:
        # empty list
        total_results = []
        # url
        url = 'https://swapi.dev/api/' + str(topic)
        # grab the search results
        response = requests.get(url)
        data = response.json()
        # Store the first page
        total_results = total_results + data['results']

        while data['next'] is not None:
            response = requests.get(data['next'])
            data = response.json()
            total_results = total_results + data['results']

            df = pd.DataFrame(total_results)
        # convert into csv and save   
        df.to_csv(f'{topic}.csv')

    return df



def grab_power_api_df(url, name):
    '''simple pull from csv format to dataframe
    'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv', 'opsd_germany_daily.csv'
    '''
    filename = (f'{name}.csv')
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=[0])
    else:
        url = url
        df = pd.read_csv(url)
        df.to_csv(f'{name}.csv')
    return df

def get_store_data():
    '''
    Returns a dataframe of all store data in the tsa_item_demand database and saves a local copy as a csv file.
    '''
    filename = "tsa_store_data.csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        query = '''
            SELECT *
            FROM items
            JOIN sales USING(item_id)
            JOIN stores USING(store_id)
            '''
        connection = get_db_url('tsa_item_demand')
        df = pd.read_sql(query, connection)
        df.to_csv(filename, index=False)
    return df
    
def check_columns(df):
    """
    This function takes a pandas dataframe as input and returns
    a dataframe with information about each column in the dataframe. For
    each column, it returns the column name, the number of
    unique values in the column, the unique values themselves,
    the number of null values in the column, and the data type of the column.
    The resulting dataframe is sorted by the 'Number of Unique Values' column in ascending order.
​
    Args:
    - df: pandas dataframe
​
    Returns:
    - pandas dataframe
    """
    data = []
    # Loop through each column in the dataframe
    for column in df.columns:
        # Append the column name, number of unique values, unique values, number of null values, and data type to the data list
        data.append(
            [
                column,
                df[column].nunique(),
                df[column].unique(),
                df[column].isna().sum(),
                df[column].isna().mean(),
                df[column].dtype
            ]
        )
    # Create a pandas dataframe from the data list, with column names 'Column Name', 'Number of Unique Values', 'Unique Values', 'Number of Null Values', and 'dtype'
    # Sort the resulting dataframe by the 'Number of Unique Values' column in ascending order
    return pd.DataFrame(
        data,
        columns=[
            "Column Name",
            "Number of Unique Values",
            "Unique Values",
            "Number of Null Values",
            "Proportion of Null Values",
            "dtype"
        ],
    ).sort_values(by="Number of Unique Values")