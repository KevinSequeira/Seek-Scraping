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

## ========================================================================== ##
## Define functions for scraping through the data.                            ##
## ========================================================================== ##
def getLatestJobs():
    """
    This function returns a table of jobs already scraped from SEEK.com.au with
    the latest listing date for different search strings.
    """
    pass

def scrapeSearchResults(latestDate: datetime, searchString: str):
    """
    This function takes in two parameters, the latest date up to which jobs
    are to be scraped, and the search string to be entered in the search bar.
    The function outputs a dataFrame of all jobs scraped up to the latest date
    for the given search string.

    Function parameters are given as:
    latestDate -> datetime.datetime
    searchString -> str

    Function returns:
    jobsDataFrame -> pandas.DataFrame
    """
    pass
