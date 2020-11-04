# Check the working directory for the project.
import os
os.getcwd()

# Import all necessary packages for the project.
import subprocess as sp
sp.call(["pip3", "install", "requests"])
import requests
sp.call(["pip3", "install", "beautifulsoup4"])
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta
sp.call(["pip3", "install", "pandas"])
import pandas as pan

## Fetch the job search for "Data Scientist".
jobSearchStrings = ["Data Scientist", "Data Science Consultant"]
dataScientistJobs = []
for searchString in jobSearchStrings:
    searchStringURL = "-".join([text.lower() for text in searchString.split(" ")]) + "-jobs"
    print(searchStringURL)
    pageCount = 1
    stopIteration = "No"
    while True:
        dataScientistPosts= requests.get("https://www.seek.com.au/" + searchStringURL + "?page=" + str(pageCount) + "&sortmode=ListedDate").text
        soupObject = BeautifulSoup(dataScientistPosts, "html.parser")
        allPageArticles = soupObject.find("div", {"data-automation": "searchResults"}).find_all("article")
        for article in allPageArticles:
            jobPost = requests.get("https://www.seek.com.au/job/" + article["data-job-id"]).text
            jobSoupObject = BeautifulSoup(jobPost, "html.parser")
            scriptWithPostIDs = jobSoupObject.find("script", text = re.compile("window.SEEK_REDUX_DATA"))
            jsonText = re.search(r'^\s*window\.SEEK_REDUX_DATA\s*=\s*({.*?})\s*;\s*$',
                          scriptWithPostIDs.string, flags = re.DOTALL | re.MULTILINE).group(1)
            jsonText = jsonText.replace(': null', ': "null"').replace(': false', ': false"').replace(': true', ': "true"').replace('undefined', '"undefined"')
            date001 = datetime.strptime(" ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5], "%Y-%m-%d %H:%M:%S")
            # print(date001.strftime('%w'))
            if (article["data-automation"] == "premiumJob"):
                if ((((datetime(2020, 11, 2, 23, 59, 59, 99999) - date001).days) > 7) | (datetime(2020, 11, 2, 23, 59, 59, 99999) < date001)):
                    continue
            elif (article["data-automation"] != "premiumJob"):
                if (((datetime(2020, 11, 2, 23, 59, 59, 99999) - date001).days) > 7):
                    stopIteration = "Yes"
                    break
                elif (datetime(2020, 11, 2, 23, 59, 59, 99999) < date001):
                    continue
            dataScientistJobs.append({"job-id": article["data-job-id"],
                                    "search-string": searchString,
                                    "job-title": json.loads(jsonText)["jobdetails"]["result"]["title"].strip(),
                                    "job-listing-date": " ".join(json.loads(jsonText)["jobdetails"]["result"]["listingDate"].split("T"))[:-5],
                                    "job-url": "https://www.seek.com.au/job/" + article["data-job-id"]})
        if stopIteration == "Yes":
            break
        pageCount += 1

# Display the dataset scraped
# dataScientistJobs = pan.DataFrame(dataScientistJobs)
# dataScientistJobs
