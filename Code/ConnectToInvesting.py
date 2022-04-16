from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


try:
    os.mkdir('data')
    print('Directory created')
except FileExistsError:
    print('Directory already exists')

print('----------------')


def enter_date(driver, date_position, date):
    date_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, date_position)))
    date_field.clear()
    date_field.send_keys(date)


class ConnectToInvesting:
    def __init__(self, url: str, connection_options: list = None):
        self.webdriver_options = Options()
        if connection_options is None:
            connection_options = ['--headless', 'window-size=1920,1080', '--no-sandbox', '--disable-dev-shm-usage',
                                  '--disable-notifications']
        self.asset_name = url.split('/')[-1]
        self.url = url+'-historical-data'
        self.connection_options = connection_options

    def connectivity_options(self):

        for option in self.connection_options:
            self.webdriver_options.add_argument(option)

    def save_data(self, data):
        file_name = self.asset_name
        with open('data/{}.csv'.format(file_name), 'w') as f:
            f.write(data)

    def connection(self, start_date='01/01/2020', end_date='12/31/2020', save_file=True, print_data=False):
        self.connectivity_options()
        with webdriver.Chrome(ChromeDriverManager().install(), options=self.webdriver_options) as driver:
            driver.get(self.url)
            print('Connected to {}'.format(self.url))
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
            print('Date range sent!')
            time.sleep(5)

            # Retrieve desired data
            data = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'curr_table')))
            print('Data received!')

            if save_file:
                print('Saving data...')
                self.save_data(data.text)
                print('Data saved!')
                print('----------------')

            if print_data:
                print(data.text)
            driver.close()


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
