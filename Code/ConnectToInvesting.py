from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
import warnings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from MissingDates import *

# Get rid of warning messages
warnings.filterwarnings("ignore")

# Create the directory where the CSVs are going to be stored; If it is already created, pass
try:
    os.mkdir('data')
    print('Directory created')
except FileExistsError:
    print('Directory already exists')

print('----------------')


# Function for sending the desired dates in the date form
def enter_date(driver, date_position, date):
    # Wait until the date element appears
    date_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, date_position)))
    # Clear the date form
    date_field.clear()
    # Send the desired dates
    date_field.send_keys(date)


# Function for translating the date format to MM/DD/YYYY
def date_translator(original_date):
    months_dict = {
        "Jan": "1,",
        "Feb": "2,",
        "Mar": "3,",
        "Apr": "4,",
        "May": "5,",
        "Jun": "6,",
        "Jul": "7,",
        "Aug": "8,",
        "Sep": "9,",
        "Oct": "10,",
        "Nov": "11,",
        "Dec": "12,"
    }
    month_string = original_date.split()[0]
    month_number = ""
    for month in months_dict:
        if month == month_string:
            month_number = months_dict.get(month)
    date_number = original_date.replace(month_string, month_number).replace(",", "/").replace(" ", "")
    return date_number


# Create a class that contains the methods to manage the data extraction application.
class ConnectToInvesting:
    def __init__(self, url: str, connection_options: list = None):
        self.webdriver_options = Options()
        if connection_options is None:
            # Define the webdriver connection options
            connection_options = ['--headless', 'window-size=1920,1080', '--no-sandbox', '--disable-dev-shm-usage',
                                  '--disable-notifications', 'log-level=3']
        # Store the name and URL of the asset
        self.asset_name = url.split('/')[-1]
        self.url = url + '-historical-data'
        self.connection_options = connection_options

    # Add the connection options to the webdriver
    def connectivity_options(self):
        for option in self.connection_options:
            self.webdriver_options.add_argument(option)

    # Save the dataframe in a csv file and store it inside the data folder
    def save_data(self, df):
        file_name = self.asset_name
        df.to_csv('data/{}.csv'.format(file_name), sep=";", index=False)

    # Establish the connection and extract the required data
    def connection(self, start_date='01/01/2020', end_date='12/31/2020', save_file=True, print_data=False):
        # Add the connection options to the webdriver
        self.connectivity_options()

        # Connect to the asset URL
        with webdriver.Chrome(ChromeDriverManager().install(), options=self.webdriver_options) as driver:
            driver.get(self.url)
            print('Connected to {}'.format(self.url))
            # Manage the cookies
            try:
                driver.find_element_by_id('onetrust-accept-btn-handler').click()
                print('Cookies accepted!')
            except NoSuchElementException:
                print('No cookies asked!')
            delay = 5

            # Clicking on the date button
            WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, 'widgetFieldDateRange'))).click()
            print('Entering date range...')

            # Sending the start date
            enter_date(driver, 'startDate', start_date)

            # Sending the end date
            enter_date(driver, 'endDate', end_date)

            # Clicking on the apply button
            apply_button = driver.find_element_by_id('applyBtn')
            apply_button.click()
            print('Date range sent!!')
            time.sleep(5)

            # Retrieve the table data
            webtable_df = pd.read_html(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'curr_table'))).get_attribute('outerHTML'))[0]
            df = pd.DataFrame(data=webtable_df['Date'], columns=['Date'])
            df['Price'] = webtable_df['Price']
            df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)

            # Store the retrieved data in a pandas Dataframe
            df = create_missing_dates(df)
            df = interpolate_df(df, self.asset_name)
            df = return_to_normal(df)

            print('Data received!!')

            if save_file:
                print('Saving data...')
                self.save_data(df)
                print('Data saved!!')
                print('----------------')

            if print_data:
                print(df)
            driver.close()


# URLs to be scraped
assets_url = ['https://www.investing.com/funds/amundi-msci-wrld-ae-c',
              'https://www.investing.com/etfs/ishares-global-corporate-bond-$',
              'https://www.investing.com/etfs/db-x-trackers-ii-global-sovereign-5',
              'https://www.investing.com/etfs/spdr-gold-trust',
              'https://www.investing.com/indices/usdollar']

print('Starting webscraping!!')
print('----------------')
print('----------------')
for asset_url in assets_url:
    ConnectToInvesting(asset_url).connection()

print('Process finished!')
