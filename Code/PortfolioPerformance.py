import pandas as pd
import numpy as np


class PortfolioPerformance:
    """
    Class for computing the performance (return and volatility) for the different portfolios.
    """
    def __init__(self, st_path='data/amundi-msci-wrld-ae-c.csv', cb_path='data/ishares-global-corporate-bond-$.csv',
                 pb_path='data/db-x-trackers-ii-global-sovereign-5.csv', go_path='data/spdr-gold-trust.csv',
                 ca_path='data/usdollar.csv', portfolios_path='data/portfolio_allocations.csv'):
        """
        Initialization function. Takes as parameter the name of the files where the data is store, five for financial
        data and the last one with the different portfolios. The las file of the data must be the dollar.
        """
        print('Loading the data...')
        self.st_data = pd.read_csv(st_path, sep=';')
        self.cb_data = pd.read_csv(cb_path, sep=';')
        self.pb_data = pd.read_csv(pb_path, sep=';')
        self.go_data = pd.read_csv(go_path, sep=';')
        self.ca_data = pd.read_csv(ca_path, sep=';')
        self.portfolios_file = pd.read_csv(portfolios_path)
        self.initial_price = []
        print('Data loaded!!')
        print('---------------------')

    def get_initial_price(self):
        """
        Function for computing the initial price for the different assets. The price for the dollar is always one.
        The function will store the values in an attribute of the class.
        """
        print('Obtaining initial price for each asset...')
        self.initial_price.extend([self.st_data.iloc[-1]['Price'], self.cb_data.iloc[-1]['Price'],
                                   self.pb_data.iloc[-1]['Price'], self.go_data.iloc[-1]['Price'], 1])
        print('Initial price obtained!!')
        print('---------------------')


    def compute_shares_number(self):
        """
        Function for computing the number of share of each asset than can be bought with the different portfolio
        configurations. As it is permitted to buy part of shares the number initial investment is 1, as it will easy the
        computation.
        """
        print('Computing number of shares per portfolio and asset...')
        self.portfolios_file['ST_shares'] = self.portfolios_file['ST'] / self.initial_price[0]
        self.portfolios_file['CB_shares'] = self.portfolios_file['CB'] / self.initial_price[1]
        self.portfolios_file['PB_shares'] = self.portfolios_file['PB'] / self.initial_price[2]
        self.portfolios_file['GO_shares'] = self.portfolios_file['GO'] / self.initial_price[3]
        self.portfolios_file['CA_shares'] = self.portfolios_file['CA'] / self.initial_price[4]
        print('Shares computed!!')
        print('---------------------')

    def compute_return(self):
        """
        Function for computing the return performance of each portfolio.
        """
        print('Computing return for each portfolio...')
        # Generating a new column in the dataframe for storing the total initial value for each portfolio
        # In the case of the dollar the price column is divided by 100.
        self.portfolios_file['initial_value'] = self.portfolios_file['ST_shares'] * self.initial_price[0] + \
                                                self.portfolios_file['CB_shares'] * self.initial_price[1] + \
                                                self.portfolios_file['PB_shares'] * self.initial_price[2] + \
                                                self.portfolios_file['GO_shares'] * self.initial_price[3] + \
                                                self.portfolios_file['CA_shares'] * self.initial_price[4]

        # Generating a new column in the dataframe for storing the total final value for each portfolio
        # In the case of the dollar the price column is divided by 100.
        self.portfolios_file['final_value'] = self.portfolios_file['ST_shares'] * self.st_data.Price.iloc[0] + \
                                              self.portfolios_file['CB_shares'] * self.cb_data.Price.iloc[0] + \
                                              self.portfolios_file['PB_shares'] * self.pb_data.Price.iloc[0] + \
                                              self.portfolios_file['GO_shares'] * self.go_data.Price.iloc[0] + \
                                              self.portfolios_file['CA_shares'] * self.ca_data.Price.iloc[0] / 100

        # Computing the return value for each portfolio:
        # return = (final_value - initial_value) / initial_value * 100
        self.portfolios_file['RETURN'] = (self.portfolios_file['final_value'] - self.portfolios_file['initial_value']) \
                                         / self.portfolios_file['initial_value'] * 100
        # Dropping the initial and final values columns as they are not necessary anymore.
        self.portfolios_file = self.portfolios_file.drop(['initial_value', 'final_value'], axis=1)
        print('Return computed!!')
        print('---------------------')

    def compute_volatility(self):
        """
        Function for computing the volatility performance of each portfolio.
        """
        print('Computing volatility for each portfolio...')

        # Create an empty column with the volatility
        self.portfolios_file['VOLATILITY'] = np.nan
        # Lop for each one fo the portfolios.
        for portfolio in range(len(self.portfolios_file)):
            values = []
            # Lop for each one of the date in the financial dataframe for computing the value for each date and each
            # asset. The dollar is divided by 100.
            for date in range(len(self.st_data)):
                st_value = self.portfolios_file['ST_shares'].iloc[portfolio] * self.st_data['Price'].iloc[date]
                cb_value = self.portfolios_file['CB_shares'].iloc[portfolio] * self.cb_data['Price'].iloc[date]
                pb_value = self.portfolios_file['PB_shares'].iloc[portfolio] * self.pb_data['Price'].iloc[date]
                go_value = self.portfolios_file['GO_shares'].iloc[portfolio] * self.go_data['Price'].iloc[date]
                ca_value = self.portfolios_file['CA_shares'].iloc[portfolio] * self.ca_data['Price'].iloc[date] / 100
                # Compute the total value for each date by summing the values.
                total_value = st_value + cb_value + pb_value + go_value + ca_value
                values.append(total_value)

            # Compute the volatility for each portfolio:
            # volatility = standard_deviation(value) / mean(value) * 100
            self.portfolios_file['VOLATILITY'].iloc[portfolio] = np.std(values) / np.mean(values) * 100

        print('Volatility computed!!')
        print('---------------------')

    def save_file(self, file_path, file_name):
        """
        Function for saving the file with the portfolio performance (return and volatility).
        Arguments:
            file_path: path to the folder to store the .csv file
            file_name: name of the file to be saved.
        """
        print('Saving file...')
        self.portfolios_file = self.portfolios_file.drop(['ST_shares', 'CB_shares', 'PB_shares', 'GO_shares',
                                                          'CA_shares'], axis=1)
        self.portfolios_file.to_csv(file_path + file_name, index=False)
        print('File saved!!')
        print('---------------------')


portfolio_data = PortfolioPerformance()
portfolio_data.get_initial_price()
portfolio_data.compute_shares_number()
portfolio_data.compute_return()
portfolio_data.compute_volatility()
portfolio_data.save_file('data/', 'portfolio_metrics.csv')