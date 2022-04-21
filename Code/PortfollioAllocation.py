import pandas as pd
import numpy as np
import itertools


def save_file(data: pd.DataFrame, file_name: str = 'portfolio_allocations.csv', file_path: str = 'data'):
    """
    Function for saving the generated file.
    :param data: data to be saved with the portfolio configuration. Must be a DataFrame object.
    :param file_name: str, name of the file to be saved.
    :param file_path: str, path to the place to save the file.
    """
    complete_path = file_path + '/' + file_name
    data.to_csv(complete_path, index=False)


class PortfolioAllocation:
    """
    Class for generating the different portfolio options.
    """
    def __init__(self, asset_names: list = None, increment: float = 1 / 5):
        """
        Init function for the class.
        :param asset_names: list of asset names, if not provided use the default ones (the one required for the task)
        :param increment: Increment to be used for asset distribution, if not provided use the default for the task.
        """
        if asset_names is None:
            asset_names = ['ST', 'CB', 'PB', 'GO', 'CA']
        self.asset_names = asset_names
        self.increment = increment
        self.invest_options = None

    def generate_invest_options(self):
        """
        Function for generate the different options for the portfolios.
        The code will generate all the possible combination and will save only the ones that sum up to 1.
        For this it uses the increment for the step in the np.arange function and the number of assets for the repeat
        in the itertools.product.
        The options are stored in the self.invest_options variable.
        """
        self.invest_options = []
        print('Generating different portfolio options...')

        for i in itertools.product(np.arange(1.0, 0 - self.increment, -self.increment),
                                   repeat=len(self.asset_names)):
            i = np.round(i, 1)
            if sum(i) == 1:
                self.invest_options.append(i)
        print('Portfolios generated!!')
        print('---------------------')

    def portfolio_allocation(self):
        """
        Function that will return the a dataframe with the different portfolio configurations.
        :return: dataframe with the different portfolio configuration.
        """
        self.generate_invest_options()
        return pd.DataFrame(self.invest_options, columns=self.asset_names)


portfolio = PortfolioAllocation().portfolio_allocation()
save_file(portfolio)
print('Portfolio options saved!')
