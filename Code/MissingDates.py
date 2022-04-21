# https://stackoverflow.com/questions/19324453/add-missing-dates-to-pandas-dataframe
import pandas as pd
import os
import datetime as dt
import numpy as np


def load_dataset(file_path):
    return pd.read_csv(file_path, sep=';')


# Generate a new dataframe with the missing dates
def create_missing_dates(df):
    # Covert Date column to DateTime type
    df['Date'] = pd.to_datetime(df['Date'])
    # Change the datetime format to DD-MM-YYYY for future operations
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
    # Reverse the order of the Date column
    df['Date'] = df['Date'].values[::-1]
    df['Price'] = df['Price'].values[::-1]
    # Set the Date as the new index
    df = df.set_index(df['Date'], verify_integrity=True)
    # Drop the Date column
    df = df.drop('Date', 1)
    # Reindex the dataframe to place the missing dates
    date_range = pd.date_range('01-01-2020', '12-31-2020').strftime('%d-%m-%Y')
    df = df.reindex(date_range)
    # If the first or last value of the dataframe stills be NaN, set it equals to the nearest not NaN value
    if np.isnan(df['Price'].iloc[0]):
        df['Price'].iloc[0] = df['Price'].iloc[1]
    if np.isnan(df['Price'].iloc[-1]):
        df['Price'].iloc[-1] = df['Price'].iloc[-2]
    # The resulting dataframe will have the missing dates with NaN values placed at its columns
    return df


# Use interpolation to get rid of NaN values
def interpolate_df(df, csv_name):
    # Use linear interpolation
    df = df.interpolate()
    df['Price'] = df['Price'].round(2)
    # Add the last character to the Change column
    """last_char = ''
    if csv_name == 'amundi-msci-wrld-ae-c':
        last_char = '%'
    elif csv_name == 'db-x-trackers-ii-global-sovereign-5' or csv_name == 'ishares-global-corporate-bond-$':
        last_char = 'K'
    elif csv_name == 'spdr-gold-trust':
        last_char = 'M'
    df[change] = df[change].astype(str) + last_char"""
    return df


# Modify the resulting data frame to have the initial format
def return_to_normal(df):
    # Set the index as the Date column and reset the index
    df['Date'] = df.index
    df = df.reset_index().drop('index', 1)
    df['Date'] = df['Date'].values[::-1]
    df['Price'] = df['Price'].values[::-1]
    return df


# Load the datasets
'''csv_name_list = ['amundi-msci-wrld-ae-c.csv', 'db-x-trackers-ii-global-sovereign-5.csv',
                 'ishares-global-corporate-bond-$.csv', 'spdr-gold-trust.csv', 'usdollar.csv']

for file_name in csv_name_list:
    complete_path = os.path.join("data", file_name)
    data = load_dataset(complete_path)
    data = create_missing_dates(data)
    data = interpolate_df(data, file_name)
    data = return_to_normal(data)
    with open('data/{}'.format(file_name), 'w') as f:
        data.to_csv('data/{}'.format(file_name), sep=";", index=False)'''
