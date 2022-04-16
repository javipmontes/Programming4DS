from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

#Construct a dictionary with all the URLs that we have to access
url_dict = {"stocks": "https://www.investing.com/funds/amundi-msci-wrld-ae-c-historical-data",
            "corporate bonds": "https://www.investing.com/etfs/ishares-global-corporate-bond-$-historical-data", 
            "public bonds": "https://www.investing.com/etfs/db-x-trackers-ii-global-sovereign-5-historical-data", 
            "gold": "https://www.investing.com/etfs/spdr-gold-trust-historical-data", 
            "cash": "https://www.investing.com/indices/usdollar-historical-data"}

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())