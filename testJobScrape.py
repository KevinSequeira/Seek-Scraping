# Check the working directory for the project.
import os
print(os.getcwd())

# Import all necessary packages for the project.
import subprocess as sp
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta
import pandas as pan

jobPost = requests.get("https://www.seek.com.au/job/50707174?type=standout#searchRequestToken=6bf7699b-eeca-4240-ac34-e7673b9b2443").text
jobSoupObject = BeautifulSoup(jobPost, "html.parser")
scriptWithPostIDs = jobSoupObject.find("script", text = re.compile("window.SEEK_REDUX_DATA"))
jsonText = re.search(r'^\s*window\.SEEK_REDUX_DATA\s*=\s*({.*?})\s*;\s*$',
              scriptWithPostIDs.string, flags = re.DOTALL | re.MULTILINE).group(1)
jsonText = jsonText.replace(': null', ': "null"').replace(': false', ': false"').replace(': true', ': "true"').replace('undefined', '"undefined"')
print(json.loads(jsonText)["jobdetails"]["result"])
print("job-id:", json.loads(jsonText)["jobdetails"]["result"]["id"])
print("job-title:", json.loads(jsonText)["jobdetails"]["result"]["title"])
print("job-advertiser:", json.loads(jsonText)["jobdetails"]["result"]["advertiser"]["searchParams"]["keywords"])
print("job-location-state:", json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["state"])
print("job-location-city:", json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["city"])
print("job-location-area:", json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["area"])
print("job-location-suburb:", json.loads(jsonText)["jobdetails"]["result"]["locationHierarchy"]["suburb"])
print("job-classification:", json.loads(jsonText)["jobdetails"]["result"]["classification"]["description"])
print("job-sub-classification:", json.loads(jsonText)["jobdetails"]["result"]["subClassification"]["description"])
print("job-role-titles:", json.loads(jsonText)["jobdetails"]["result"]["roleTitles"])
