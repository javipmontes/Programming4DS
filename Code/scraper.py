from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

url_dict = {}

url = "https://www.investing.com/etfs/db-x-trackers-ii-global-sovereign-5"

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

driver.get(url)