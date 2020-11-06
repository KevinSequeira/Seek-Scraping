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
    jobSearchStrings = {"Data Science": ["\"Senior Data Scientist\"", "\"Data Scientist\""],
                        "Data Analysis": ["\"Senior Data Analyst\"", "\"Data Analyst\"", "\"Graduate Data Analyst\""],
                        "Data Engineering": ["\"Senior Data Engineer\"", "\"Data Engineer\""],
                        "Data Architect": ["\"Data Architect\""],
                        "Business Intelligence": ["\"Business Intelligence Developer\"", "\"BI Developer\"", "\"Business Intelligence Specialist\"", "\"BI Specialist\"", "\"Business Intelligence Analyst\"", "\"BI Analyst\""],
                        "Machine Learning": ["\"Machine Learning Engineer\"", "\"Junior Machine Learning Engineer\"", "\"Graduate Machine Learning Engineer\""],
                        "Data Visualization": ["\"Data Visualization Developer\""],
                        "ETL Development": ["\"ETL Developer\"", "\"Junior ETL Developer\"", "\"Graduate ETL Developer\""],
                        "Database Administration": ["\"Senior Database Developer\"", "\"Database Developer\"", "\"Senior Database Administrator\"", "\"Database Administrator\""],
                        "Cloud Development": ["\"Cloud Developer\"", "\"Cloud Engineer\""]}
    return jobSearchStrings

def getLatestJobs():
    """
    This function returns a table of jobs already scraped from SEEK.com.au with
    the latest listing date for different search strings.
    """
    pass

def getJobDetails(article, latestDate: datetime, domain: str, searchString: str, getFullDetails: str = "no"):
    """

    """
    jobPost = requests.get("https://www.seek.com.au/job/" + article["data-job-id"]).text
    jobSoupObject = BeautifulSoup(jobPost, "html.parser")
    scriptWithPostIDs = jobSoupObject.find("script", text = re.compile("window.SEEK_REDUX_DATA"))
    jsonText = re.search(r'^\s*window\.SEEK_REDUX_DATA\s*=\s*({.*?})\s*;\s*$',
                  scriptWithPostIDs.string, flags = re.DOTALL | re.MULTILINE).group(1)
    jsonText = jsonText.replace(': null', ': "null"').replace(': false', ': false"').replace(': true', ': "true"').replace('undefined', '"undefined"')
    listingDate = datetime.strptime(" ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5], "%Y-%m-%d %H:%M:%S")
    # print(date001.strftime('%w'))
    if (latestDate < listingDate):
        print(listingDate)
        return None
    if getFullDetails == "no":
        return {"job-id": article["data-job-id"],
                "job-domain": domain,
                "search-string": searchString,
                "job-title": json.loads(jsonText)["jobdetails"]["result"]["title"].strip(),
                "job-listing-date": " ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5],
                "job-url": "https://www.seek.com.au/job/" + article["data-job-id"]}
    elif getFullDetails == "yes":
        # print(searchString, article["data-job-id"], json.loads(jsonText)["jobdetails"]["result"]["title"].strip())
        return {"job-id": article["data-job-id"],
                "job-title": json.loads(jsonText)["jobdetails"]["result"]["title"].strip(),
                "job-listing-date": " ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5],
                "job-url": "https://www.seek.com.au/job/" + article["data-job-id"]}

def scrapeSearchResults(latestDate: datetime, domain: str, searchString: str, jobsIDList: list = []):
    """
    This function takes in three parameters, the latest date up to which jobs
    are to be scraped, and the search string to be entered in the search bar.
    The function outputs a dataframe of all jobs scraped up to the latest date
    for the given search string.

    Function parameters are given as:
    latestDate -> datetime
    domain -> str
    searchString -> str
    jobsIDList -> list

    Function returns:
    jobsDataFrame -> pandas.DataFrame
    jobsMasterDataFrame -> pandas.DataFrame
    """
    searchStringURL = "%20".join([text for text in searchString.split(" ")])
    jobsList = []
    jobsMasterList = []
    pageCount = 1
    stopIteration = "No"
    while True:
        jobPosts= requests.get("https://www.seek.com.au/jobs?classification=1209%2C1210%2C6281%2C1223&keywords=" + searchStringURL + "&page=" + str(pageCount) + "&sortmode=ListedDate").text
        soupObject = BeautifulSoup(jobPosts, "html.parser")
        allPageArticles = soupObject.find("div", {"data-automation": "searchResults"})
        if allPageArticles != None:
            allPageArticles = allPageArticles.find_all("article")
            if len(allPageArticles) == 0:
                break
        else:
            break
        for article in allPageArticles:
            if article["data-automation"] == "premiumJob":
                continue
            jobDict = getJobDetails(article = article,
                                    latestDate = latestDate,
                                    domain = domain,
                                    searchString = searchString,
                                    getFullDetails = "no")
            if jobDict is not None:
                jobsList.append(jobDict)
                if jobDict["job-id"] not in jobsIDList:
                    jobsMasterList.append(getJobDetails(article = article,
                                            latestDate = latestDate,
                                            domain = domain,
                                            searchString = searchString,
                                            getFullDetails = "yes"))
                    jobsIDList.append(jobDict["job-id"])
        if stopIteration == "Yes":
            break
        pageCount += 1

    return pan.DataFrame(jobsList), pan.DataFrame(jobsMasterList), jobsIDList

def loopOverRoles(latestDate: datetime, scrapedJobs: pan.DataFrame, scrapedJobsMaster: pan.DataFrame, jobRoles: dict):
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
    scrapedJobsMaster -> pandas.DataFrame
    jobsIDMasterList -> list
    """
    jobsIDMasterList = []
    for domain, searchStrings in jobRoles.items():
        for searchString in searchStrings:
            print("Domain:", domain + ",", "Search String:", searchString)
            print("Number of jobs:", len(jobsIDMasterList))
            jobsDataFrame, jobsMasterDataFrame, jobsIDList = scrapeSearchResults(latestDate = latestDate,
                domain = domain,
                searchString = searchString,
                jobsIDList = jobsIDMasterList)
            scrapedJobs = scrapedJobs.append(jobsDataFrame)
            scrapedJobsMaster = scrapedJobsMaster.append(jobsMasterDataFrame)
            jobsIDMasterList = jobsIDMasterList
            print("Number of jobs:", len(jobsIDMasterList))

    return scrapedJobs, scrapedJobsMaster

if __name__ == '__main__':
    scrapedJobs = pan.DataFrame(columns=["job-id", "job-domain", "search-string",
                                         "job-title", "job-listing-date", "job-url"])
    scrapedJobsMaster = pan.DataFrame(columns=["job-id", "job-title", "job-listing-date", "job-url"])
    jobSearchStrings = initializeVariables()
    dataJobsDataframe, dataJobsMasterDataFrame = loopOverRoles(latestDate = datetime(2020, 11, 5, 23, 59, 59, 99999),
        scrapedJobs = scrapedJobs,
        scrapedJobsMaster = scrapedJobsMaster,
        jobRoles = jobSearchStrings)
    dataJobsDataframe.to_csv("Seek Data Jobs.csv", index = False)
    dataJobsMasterDataFrame.to_csv("Seek Data Jobs Master.csv", index = False)
