# Programming4DS
Main repository for the development of the Programming for Data Science final assignment.
---------------------
Description of contents:
Repository:
    Code folder:
        Data folder:
            This folder contains the different .csv files generated and needed for the work developed.
        ConnectToInvesting.py: this python file contains the implementation of the webscraping tool.
        MissingDates.py: this python files contains the code for dealing with missing dates in the .csv files.
        PortfolioPerformance.py: this python files contains the code for computing each portfolio performance
            (return and volatility measures).
        PortfolioAllocation.py: this python files contains the code for generating the different asset combination
            for each portfolio.
        ReturnAnalysis.ipynb: this jupyter notebook contains the data analysis performed for the return performance
    README.md
    requirement.txt: this file provides a list of the packages that are needed for the user to run the code.

---------------------
### How to run:

1. Run the ConnectToInvesting.py file. This file will generate the 5 csv files that contains the date, price and change
values for the asset. It has a class that allows to deal with the url for the scrapping. It takes as argument the URL
for the main page of the asset in the format https://www.investing.com/indices/ASSET (the "-historical-data" part is
added by the class). It has a method for retrieving the data that allows some parameters like start and end date. This
file will also deal with the missing dates by calling the implementation developed for it in the MissingDates.py file.

2. Run the PortfolioAllocation.py file. This file implement a class for generating the different portfolios based on
the asset available and the percentage increment (by default the arguments are fixed to the ones required for the task,
but it can be changed by adding asset_names and increment) This will generate the portfolio_allocation.csv file.

3. Run the PortfolioPerformance.py file. This file implements the computation of the two metrics selected, return and
volatility. It uses the different portfolio configuration data from the portfolio_allocation.csv to generate a new file
with the return and volatility columns for each portfolio called portfolio_metrics.csv.

4. Run or see the ReturnAnalysis.ipynb file. This file uses the portfolio_metrics.csv file to generate the different plots
needed for assessing the questions related to the Return part of the strategies' analysis. It will generate a histogram,
a distribution plot and a box plot graphics.

5. Run or see the ReturnAnalysis.ipynb file. This file uses the portfolio_metrics.csv file to generate different plots needed for assessing the questions related to the Return vs Risk part of the strategies' analysis. It will generate a scatterplot and different stacked bar-charts for different volatilities.

