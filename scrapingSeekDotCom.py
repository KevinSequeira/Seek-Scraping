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

## ========================================================================== ##
## Define functions for scraping through the data.                            ##
## ========================================================================== ##
def initializeVariables():
    ## Initialize a dictionary of all relevant job search strings.
    jobSearchStrings = {"Data Science": ["\"Data Scientist\"", "\"Junior Data Scientist\"", "\"Graduate Data Scientist\""],
                        "Data Analysis": ["\"Data Analyst\"", "\"Junior Data Analyst\"", "\"Graduate Data Analyst\""],
                        "Data Engineering": ["\"Data Engineer\"", "\"Junior Data Engineer\"", "\"Graduate Data Engineer\""],
                        "Business Intelligence": ["\"Business Intelligence Developer\"", "\"Junior Business Intelligence Developer\"", "\"Graduate Business Intelligence Developer\"",
                                         "\"BI Developer\"", "\"Junior BI Developer\"", "\"Graduate BI Developer\""],
                        "Machine Learning": ["\"Machine Learning Engineer\"", "\"Junior Machine Learning Engineer\"", "\"Graduate Machine Learning Engineer\""],
                        "Data Visualization": ["\"Data Visualization Developer\"", "\"Junior Data Visualization Developer\"", "\"Graduate Data Visualization Developer\""],
                        "ETL Development": ["\"ETL Developer\"", "\"Junior ETL Developer\"", "\"Graduate ETL Developer\""],
                        "Database Administration": ["\"Database Developer\"", "\"Junior Database Developer\"", "\"Graduate Database Developer\"",
                                                   "\"Database Administrator\"", "\"Junior Database Administrator\"", "\"Graduate Database Administrator\""],
                        "Cloud Development": ["\"Cloud Developer\"", "\"Junior Cloud Developer\"", "\"Graduate Cloud Developer\""],
                        "Business Analysis": ["\"Business Analyst\"", "\"Junior Business Analyst\"", "\"Graduate Business Analyst\""]}
    return jobSearchStrings

def getLatestJobs():
    """
    This function returns a table of jobs already scraped from SEEK.com.au with
    the latest listing date for different search strings.
    """
    pass

def scrapeSearchResults(latestDate: datetime, domain: str, searchString: str):
    """
    This function takes in three parameters, the latest date up to which jobs
    are to be scraped, and the search string to be entered in the search bar.
    The function outputs a dataframe of all jobs scraped up to the latest date
    for the given search string.

    Function parameters are given as:
    latestDate -> datetime
    domain -> str
    searchString -> str

    Function returns:
    jobsDataFrame -> pandas.DataFrame
    """
    searchStringURL = "%20".join([text for text in searchString.split(" ")])
    jobsList = []
    pageCount = 1
    stopIteration = "No"
    while True:
        jobPosts= requests.get("https://www.seek.com.au/jobs?daterange=999&keywords=" + searchStringURL + "&page=" + str(pageCount) + "&sortmode=ListedDate").text
        soupObject = BeautifulSoup(jobPosts, "html.parser")
        allPageArticles = soupObject.find("div", {"data-automation": "searchResults"})
        if allPageArticles != None:
            allPageArticles = allPageArticles.find_all("article")
            if len(allPageArticles) == 0:
                break
        else:
            break
        for article in allPageArticles:
            jobPost = requests.get("https://www.seek.com.au/job/" + article["data-job-id"]).text
            jobSoupObject = BeautifulSoup(jobPost, "html.parser")
            scriptWithPostIDs = jobSoupObject.find("script", text = re.compile("window.SEEK_REDUX_DATA"))
            jsonText = re.search(r'^\s*window\.SEEK_REDUX_DATA\s*=\s*({.*?})\s*;\s*$',
                          scriptWithPostIDs.string, flags = re.DOTALL | re.MULTILINE).group(1)
            jsonText = jsonText.replace(': null', ': "null"').replace(': false', ': false"').replace(': true', ': "true"').replace('undefined', '"undefined"')
            listingDate = datetime.strptime(" ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5], "%Y-%m-%d %H:%M:%S")
            # print(date001.strftime('%w'))
            if (latestDate < listingDate):
                continue
            print(searchString, article["data-job-id"], json.loads(jsonText)["jobdetails"]["result"]["title"].strip())
            jobsList.append({"job-id": article["data-job-id"],
                            "job-domain": domain,
                            "search-string": searchString,
                            "job-title": json.loads(jsonText)["jobdetails"]["result"]["title"].strip(),
                            "job-listing-date": " ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5],
                            "job-url": "https://www.seek.com.au/job/" + article["data-job-id"]})
        if stopIteration == "Yes":
            break
        pageCount += 1

    return pan.DataFrame(jobsList)

def loopOverRoles(latestDate: datetime, scrapedJobs: pan.DataFrame, jobRoles: dict):
    """
    This function loops over different roles and appends all the search results
    into one dataset. The function takes in three parameters, the latest date up
    to which jobs are to be scraped, an empty dataframe to hold all jobs, and
    the dictionary of list of roles for each job.
    The function outputs a consolidate dataframe of all jobs scraped up to the
    latest date.

    Function parameters are given as:
    latestDate -> datetime
    scrapedJobs -> pandas.DataFrame
    jobRoles

    Function returns:
    scrapedJobs -> pandas.DataFrame
    """
    for domain, searchStrings in jobRoles.items():
        for searchString in searchStrings:
            print("Domain:", domain + ",", "Search String:", searchString)
            scrapedJobs = scrapedJobs.append(scrapeSearchResults(latestDate = latestDate,
                domain = domain,
                searchString = searchString))

    return scrapedJobs

if __name__ == '__main__':
    scrapedJobs = pan.DataFrame(columns=["job-id", "job-domain", "search-string",
                                         "job-title", "job-listing-date", "job-url"])
    jobSearchStrings = initializeVariables()
    dataJobsDataframe = loopOverRoles(latestDate = datetime(2020, 11, 5, 23, 59, 59, 99999),
        scrapedJobs = scrapedJobs,
        jobRoles = jobSearchStrings)
    dataJobsDataframe.to_csv("Seek Data Jobs.csv")
