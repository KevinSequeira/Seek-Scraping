## ========================================================================== ##
## Import all the necessary modules.                                          ##
## ========================================================================== ##
import subprocess as sp
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta
import pandas as pan

## ========================================================================== ##
## Initialize all the variables necessary for the data scraping process.      ##
## ========================================================================== ##
## Initialize a dictionary of all relevant job search strings.
jobSearchStrings = {"Data Science": ["Data Scientist", "Junior Data Scientist", "Graduate Data Engineer"],
                    "Data Analysis": ["Data Analyst", "Junior Data Analyst", "Graduate Data Analyst"],
                    "Data Engineering": ["Data Engineer", "Junior Data Engineer", "Graduate Data Engineer"],
                    "Business Intelligence": ["Business Intelligence Developer", "Junior Business Intelligence Developer", "Graduate Business Intelligence Developer",
                                     "BI Developer", "Junior BI Developer", "Graduate BI Developer"],
                    "Machine Learning": ["Machine Learning Engineer", "Junior Machine Learning Engineer", "Graduate Machine Learning Engineer"],
                    "Data Visualization": ["Data Visualization Developer", "Junior Data Visualization Developer", "Graduate Data Visualization Developer"],
                    "ETL Development": ["ETL Developer", "Junior ETL Developer", "Graduate ETL Developer"],
                    "Database Administration": ["Database Developer", "Junior Database Developer", "Graduate Database Developer",
                                               "Database Administrator", "Junior Database Administrator", "Graduate Database Administrator"],
                    "Cloud Development": ["Cloud Developer", "Junior Cloud Developer", "Graduate Cloud Developer"],
                    "Business Analysis": ["Business Analyst", "Junior Business Analyst", "Graduate Business Analyst"]}
## Initialize a list of strings to check for
