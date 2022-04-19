import pandas as pd
import numpy as np
import itertools


def save_file(data: pd.DataFrame, file_name: str = 'portfolio_allocations.csv', file_path: str = 'data'):
    complete_path = file_path + '/' + file_name
    data.to_csv(complete_path, index=False)


class PortfolioAllocation:
    def __init__(self, asset_names: list = None, increment: float = 1 / 5):
        if asset_names is None:
            asset_names = ['ST', 'CB', 'PB', 'GO', 'CA']
        self.asset_names = asset_names
        self.increment = increment
        self.invest_options = None

    def generate_invest_options(self):
        self.invest_options = []
        for i in itertools.product(np.arange(1.0, 0 - self.increment, -self.increment),
                                   repeat=len(self.asset_names)):
            i = np.round(i, 1)
            if sum(i) == 1:
                self.invest_options.append(i)

    def portfolio_allocation(self):
        self.generate_invest_options()
        return pd.DataFrame(self.invest_options, columns=self.asset_names)


portfolio = PortfolioAllocation().portfolio_allocation()
save_file(portfolio)
