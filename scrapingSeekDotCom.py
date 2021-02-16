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

import os
print("Working Directory:", os.getcwd())
os.chdir(os.getcwd())

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
                        "Data Architect": ["\"Senior Data Architect\"", "\"Data Architect\""],
                        "Business Intelligence": ["\"Senior Business Intelligence Developer\"", "\"Senior BI Developer\"", "\"Senior Business Intelligence Specialist\"", "\"Senior BI Specialist\"", "\"Senior Business Intelligence Analyst\"", "\"Senior BI Analyst\"",
                            "\"Business Intelligence Developer\"", "\"BI Developer\"", "\"Business Intelligence Specialist\"", "\"BI Specialist\"", "\"Business Intelligence Analyst\"", "\"BI Analyst\""],
                        "Machine Learning": ["\"Senior Machine Learning Engineer\"", "\"Machine Learning Engineer\""],
                        "Data Visualization": ["\"Data Visualization Developer\""],
                        "ETL Development": ["\"Senior ETL Developer\"", "\"ETL Developer\""],
                        "Database Administration": ["\"Senior Database Developer\"", "\"Database Developer\"", "\"Senior Database Administrator\"", "\"Database Administrator\""],
                        "Cloud Development": ["\"Senior Cloud Developer\"", "\"Senior Cloud Engineer\"", "\"Senior Cloud Architect\"", "\"Senior Cloud Consultant\"",
                            "\"Cloud Developer\"", "\"Cloud Engineer\"", "\"Cloud Architect\"", "\"Cloud Consultant\""]}
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
        return None
    if getFullDetails == "no":
        return {"job-id": article["data-job-id"],
                "job-domain": domain,
                "search-string": searchString.replace("\"", ""),
                "job-title": json.loads(jsonText)["jobdetails"]["result"]["title"].strip(),
                "job-listing-date": " ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5]}
    elif getFullDetails == "yes":
        # print(searchString, article["data-job-id"], json.loads(jsonText)["jobdetails"]["result"]["title"].strip())
        jobAdvertiser = json.loads(jsonText)["jobdetails"]["result"]["advertiser"]["description"]
        if "searchParams" in json.loads(jsonText)["jobdetails"]["result"]["advertiser"].keys():
            if "keywords" in json.loads(jsonText)["jobdetails"]["result"]["advertiser"]["searchParams"].keys():
                jobAdvertiser = json.loads(jsonText)["jobdetails"]["result"]["advertiser"]["searchParams"]["keywords"]
        else:
            jobAdvertiser = json.loads(jsonText)["jobdetails"]["result"]["advertiser"]["description"]
        jobAdvertiserEmail = ""
        jobAdvertiserPhone = ""
        contactsList = []
        if "contactMatches" in json.loads(jsonText)["jobdetails"]["result"].keys():
            if len(json.loads(jsonText)["jobdetails"]["result"]["contactMatches"]) > 0:
                for dictionary in json.loads(jsonText)["jobdetails"]["result"]["contactMatches"]:
                    if dictionary["type"] == "Email":
                        jobAdvertiserEmail = "Yes"
                        emailAddress = dictionary["value"].split(";")[-1].lower()
                        contactsList.append([article["data-job-id"], "Email", emailAddress])
                    elif dictionary["type"] == "Phone":
                        phoneNumber = dictionary["value"].replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
                        if (len(phoneNumber) == 8):
                            if (json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["state"].lower() in ["new south wales", "australian capital territory"]):
                                phoneNumber = "+61 2" + phoneNumber
                            elif (json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["state"].lower() in ["victoria", "tasmania"]):
                                phoneNumber = "+61 3" + phoneNumber
                            elif (json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["state"].lower() in ["queensland"], ):
                                phoneNumber = "+61 3" + phoneNumber
                            elif (json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["state"].lower() in ["western australia", "south australia", "nothern territory"], ):
                                phoneNumber = "+61 3" + phoneNumber
                        elif (len(phoneNumber) == 9) & (phoneNumber[0] in ("2", "3", "7", "8")):
                            phoneNumber = "+61 " + phoneNumber
                        elif (len(phoneNumber) == 10) & (phoneNumber[0] == "0"):
                            phoneNumber = "+61 " + phoneNumber[1:]
                        elif (len(phoneNumber) == 11) & (phoneNumber[0:2] == "61"):
                            phoneNumber = "+61 " + phoneNumber[2:]
                        elif (phoneNumber[0:3] == "+61"):
                            phoneNumber = phoneNumber.replace("+610", "+61").replace("+61", "+61 ")
                        if len(phoneNumber) == 8:
                            continue
                        # print(article["data-job-id"], phoneNumber)
                        jobAdvertiserPhone = "Yes"
                        contactsList.append([article["data-job-id"], "Phone", phoneNumber])
        citizenshipMentioned = ""
        if "desktopAdTemplate" in json.loads(jsonText)["jobdetails"]["result"].keys():
            adTemplate = "desktopAdTemplate"
        elif "mobileAdTemplate" in json.loads(jsonText)["jobdetails"]["result"].keys():
            adTemplate = "mobileAdTemplate"
        if "citizen" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower():
            if ("australian citizen" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower()) |\
            ("nz citizen" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower()) |\
            ("citizenship" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower()):
                citizenshipMentioned = "Yes"
        elif "clearance" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower():
            if ("security clearance" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower()) |\
            ("baseline security clearance" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower()) |\
            ("baseline clearance" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower()) |\
            ("nv1" in json.loads(jsonText)["jobdetails"]["result"][adTemplate].lower()):
                citizenshipMentioned = "Yes"
        jobDetails = {"job-id": article["data-job-id"],
            "job-title": json.loads(jsonText)["jobdetails"]["result"]["title"].strip(),
            "job-listing-date": " ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5],
            "job-url": "https://www.seek.com.au/job/" + article["data-job-id"],
            "job-location-state": json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["state"],
            "job-location-city": json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["city"],
            "job-location-area": json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["area"],
            "job-location-suburb": json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["suburb"],
            "job-citizenship-required": citizenshipMentioned,
            "job-advertiser": jobAdvertiser,
            "job-advertiser-email": jobAdvertiserEmail,
            "job-advertiser-phone": jobAdvertiserPhone,
            "job-classification": json.loads(jsonText)["jobdetails"]["result"]["classification"]["description"],
            "job-sub-classification": json.loads(jsonText)["jobdetails"]["result"]["subClassification"]["description"]}
        return jobDetails, contactsList

def scrapeSearchResults(latestDate: datetime, domain: str, searchString: str, latestTimestamp: str, jobsIDList: list = []):
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
    jobsContactsList = []
    pageCount = 1
    continueSearch = True
    while continueSearch:
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
            if jobDict["job-listing-date"] <= latestTimestamp:
                continueSearch = False
                break
            if jobDict is not None:
                jobsList.append(jobDict)
                if jobDict["job-id"] not in jobsIDList:
                    jobDetails, contactsList = getJobDetails(article = article,
                                            latestDate = latestDate,
                                            domain = domain,
                                            searchString = searchString,
                                            getFullDetails = "yes")
                    print(jobDict["job-id"], jobDict["job-listing-date"], jobDict["job-title"])
                    jobsMasterList.append(jobDetails)
                    jobsIDList.append(jobDict["job-id"])
                    jobsContactsList = jobsContactsList + contactsList
        pageCount += 1

    return pan.DataFrame(jobsList), pan.DataFrame(jobsMasterList), jobsIDList, jobsContactsList

def loopOverRoles(latestDate: datetime, scrapedJobs: pan.DataFrame, scrapedJobsMaster: pan.DataFrame, jobRoles: dict, latestTimestamps: pan.DataFrame):
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
    contactsList = []
    for domain, searchStrings in jobRoles.items():
        for searchString in searchStrings:
            print("Domain:", domain + ",", "Search String:", searchString.replace("\"", ""))
            print("Number of jobs to start:", len(jobsIDMasterList))
            latestTimestamp = latestTimestamps["latest-timestamp"][latestTimestamps["search-string"] == searchString.replace("\"", "")].tolist()[0]
            jobsDataFrame, jobsMasterDataFrame, jobsIDList, jobsContactsList = scrapeSearchResults(latestDate = latestDate,
                domain = domain,
                searchString = searchString,
                latestTimestamp = latestTimestamp,
                jobsIDList = jobsIDMasterList)
            scrapedJobs = scrapedJobs.append(jobsDataFrame)
            scrapedJobsMaster = scrapedJobsMaster.append(jobsMasterDataFrame)
            jobsIDMasterList = jobsIDMasterList
            contactsList = contactsList + jobsContactsList
            print("Number of jobs to end:", len(jobsIDMasterList))

    return scrapedJobs, scrapedJobsMaster, contactsList

if __name__ == '__main__':
    scrapedJobs = pan.DataFrame(columns=["job-id", "job-domain", "search-string", "job-title", "job-listing-date"])
    scrapedJobsMaster = pan.DataFrame(columns=["job-id", "job-title", "job-listing-date", "job-url",
                                               "job-location-state", "job-location-city", "job-location-area",
                                               "job-location-suburb", "job-advertiser", "job-advertiser-email", "job-advertiser-phone",
                                               "job-classification", "job-sub-classification"])
    try:
        scrapedJobsLatest = pan.read_csv("Scraped Jobs Latest Timestamps.csv")
    except:
        scrapedJobsLatest = pan.DataFrame([["Senior Data Scientist", "1000-01-01 00:00:00"],
                                           ["Data Scientist", "1000-01-01 00:00:00"],
                                           ["Senior Data Analyst", "1000-01-01 00:00:00"],
                                           ["Data Analyst", "1000-01-01 00:00:00"],
                                           ["Graduate Data Analyst", "1000-01-01 00:00:00"],
                                           ["Senior Data Engineer", "1000-01-01 00:00:00"],
                                           ["Data Engineer", "1000-01-01 00:00:00"],
                                           ["Senior Data Architect", "1000-01-01 00:00:00"],
                                           ["Data Architect", "1000-01-01 00:00:00"],
                                           ["Senior Business Intelligence Developer", "1000-01-01 00:00:00"],
                                           ["Senior BI Developer", "1000-01-01 00:00:00"],
                                           ["Senior Business Intelligence Specialist", "1000-01-01 00:00:00"],
                                           ["Senior BI Specialist", "1000-01-01 00:00:00"],
                                           ["Senior Business Intelligence Analyst", "1000-01-01 00:00:00"],
                                           ["Senior BI Analyst", "1000-01-01 00:00:00"],
                                           ["Business Intelligence Developer", "1000-01-01 00:00:00"],
                                           ["BI Developer", "1000-01-01 00:00:00"],
                                           ["Business Intelligence Specialist", "1000-01-01 00:00:00"],
                                           ["BI Specialist", "1000-01-01 00:00:00"],
                                           ["Business Intelligence Analyst", "1000-01-01 00:00:00"],
                                           ["BI Analyst", "1000-01-01 00:00:00"],
                                           ["Senior Machine Learning Engineer", "1000-01-01 00:00:00"],
                                           ["Machine Learning Engineer", "1000-01-01 00:00:00"],
                                           ["Data Visualization Developer", "1000-01-01 00:00:00"],
                                           ["Senior ETL Developer", "1000-01-01 00:00:00"],
                                           ["ETL Developer", "1000-01-01 00:00:00"],
                                           ["Senior Database Developer", "1000-01-01 00:00:00"],
                                           ["Database Developer", "1000-01-01 00:00:00"],
                                           ["Senior Database Administrator", "1000-01-01 00:00:00"],
                                           ["Database Administrator", "1000-01-01 00:00:00"],
                                           ["Senior Cloud Developer", "1000-01-01 00:00:00"],
                                           ["Senior Cloud Engineer", "1000-01-01 00:00:00"],
                                           ["Senior Cloud Architect", "1000-01-01 00:00:00"],
                                           ["Senior Cloud Consultant", "1000-01-01 00:00:00"],
                                           ["Cloud Developer", "1000-01-01 00:00:00"],
                                           ["Cloud Engineer", "1000-01-01 00:00:00"],
                                           ["Cloud Architect", "1000-01-01 00:00:00"],
                                           ["Cloud Consultant", "1000-01-01 00:00:00"]],
                                           columns = ["search-string", "latest-timestamp"])
    jobSearchStrings = initializeVariables()
    dataJobsDataframe, dataJobsMasterDataFrame, contactsList = loopOverRoles(latestDate = datetime.now(),
        scrapedJobs = scrapedJobs,
        scrapedJobsMaster = scrapedJobsMaster,
        jobRoles = jobSearchStrings,
        latestTimestamps = scrapedJobsLatest)
    if dataJobsDataframe.shape[0] > 0:
        dataJobsDataframe.to_csv("Seek Data Jobs.csv", mode = "a", index = False)
        dataJobsMasterDataFrame.to_csv("Seek Data Jobs Master.csv", mode = "a", index = False)
        dataFrameJobContacts = pan.DataFrame(contactsList, columns = ["job-id", "contact-type", "value"])
        dataFrameJobContacts.to_csv("Seek Data Jobs Contacts.csv", mode = "a", index = False)
    newScrapedJobsLatest = dataJobsDataframe.groupby(["search-string"], as_index = False).agg({"job-listing-date": "max"})
    scrapedJobsLatest = scrapedJobsLatest.join(newScrapedJobsLatest.set_index("search-string"), on = ["search-string"], lsuffix = "-old", rsuffix = "-new")
    scrapedJobsLatest["job-listing-date"] = scrapedJobsLatest["job-listing-date"].fillna("1000-01-01 00:00:00")
    newScrapedJobsLatest = pan.DataFrame(columns = ["search-string", "latest-timestamp"])
    newScrapedJobsLatest["search-string"] = scrapedJobsLatest["search-string"]
    newScrapedJobsLatest["latest-timestamp"] = scrapedJobsLatest[["latest-timestamp", "job-listing-date"]].apply(lambda row: max([row[0], row[1]]), axis = 1)
    newScrapedJobsLatest.to_csv("Scraped Jobs Latest Timestamps.csv", index = False)
