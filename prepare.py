# imports
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

def clean_germany_power(df):

    '''takes the germany power df after acquire and cleans'''

    df.columns = df.columns.str.lower()     # lowercase columns
    df.columns = df.columns.str.replace('+', '_')   # replace + in columns

    df.date = pd.to_datetime(df.date) # changes date into datetime

    df = df.set_index('date').sort_index() # sorts index

    # creates 2 columns, month & year
    df['month'] = df.index.month
    df['year'] = df.index.year

    df = df.fillna(0) # fills nan with 0

    # creates another wind_solar column to adjust missing values
    df['wind_and_solar'] = round(df['wind'] + df['solar'], 3)
    # drop old wind_solar column
    df.drop(columns='wind_solar', inplace=True)

    # plots hist for all columns
    plt.figure(figsize=(16,6))
    for i, col in enumerate(df.columns):
        plot_num = i+1
        plt.subplot(2,5, plot_num)
        plt.title(col)
        df[col].hist(bins=30)
        plt.grid(False)

    return df

def clean_store(df):
    '''takes the store dataframe and cleans it'''

    # change sale date to datetime
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    # sets and sorts index by sale date
    df = df.set_index('sale_date').sort_index()
    # Adds month & year columns
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day_of_week'] = df.index.day_name()
    # Adds Sales total column
    df['sales_total'] = df.sale_amount * df.item_price

    return df