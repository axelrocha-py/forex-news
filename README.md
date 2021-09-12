# Forex-News
Forex News is a project whose goal was providing updated information for the students of the GBM Homebroker trading course.

Basically it is a program that extracts information from the three best financial news sites in the world so that it subsequently goes through the ETL stages, ending with the loading of the dataset into a relational MySQL Database.

Extract: In this stage, three web scrapers developed in Python are implemented, using the BeautifulSoup library and extracting them with Pandas as CSV files with a homogeneous structure.

Transform: Now I process the data collected in CSV format and proceed to clean it (line breaks, special characters, etc.), I work with the NaN data in Pandas to add the missing fields or process them so that there is no error in the Load stage. I add a unique_id to each news using hash. A clean CSV file is obtained and ready to be loaded.

Load: Finally, using the sqlalchemy library, I load the CSV file into a MySQL relational database. I include a main.py file that automates the three ETL processes so that everything is executable through a single call to the main.py file.
