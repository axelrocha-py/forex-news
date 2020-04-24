from InvestingWebScraper import init_in
from DailyfxWebScraper import init_fx
from CurrencynewsWebScraper import init_cn
from DataWrangler import clean_data
from LoadEngine import load_data

# EXTRACT
init_in()
init_fx()
init_cn()

# TRANSFORM
clean_data()

#LOAD
load_data()