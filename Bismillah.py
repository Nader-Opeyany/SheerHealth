import requests
from bs4 import BeautifulSoup
import os
import time 
import json

nhsDict = {}
failedScrappingDict = {}
#requests to extract html and css from nhs hyperlink 
nhsMedicinePageListURL = "https://www.nhs.uk/medicines/" #constant
response = requests.get(nhsMedicinePageListURL)
nhsRawHTML = response.text
strNHSMedicineFileName = "Scrapped/nhsPageListRawHTMLText.txt"

#if file doesnt exist scrape and generate
if (not os.path.exists(strNHSMedicineFileName)):
    try:
        with open(strNHSMedicineFileName,"w",encoding="utf-8") as f:
            f.write(nhsRawHTML)
        print("Successful text scrapping and dumping\n")
    except IOError as e:
        print("Error saving scrapped NHS main List page HTML Error is : {}".format(e))


nhsScrappedFileText = ""
try:
    with open(strNHSMedicineFileName,"r",encoding="utf-8") as f:
        nhsScrappedFileText = f.read()
except IOError as e:
    print("Error saving scrapped NHS main List into variable nhsScrappedFileText : {}".format(e))

soup = BeautifulSoup(nhsScrappedFileText,'html.parser')

#Processing soup class <ul class="nhsuk-list nhsuk-list--border nhsuk-list--links">
for ul in soup.select("ul.nhsuk-list--border.nhsuk-list--links"):
    for link in ul.find_all("a"):
        tempKeyForFailedScrapping = 0
        medName = link.get_text(strip =True)
        href = link["href"]

        #add hyperlink and name of each medicine here
        if(href[0] == '/'):
            href = "https://www.nhs.uk" + href
        #if there is an extranous link or unregistered text
        else:
            failedScrappingDict[tempKeyForFailedScrapping] = href
            tempKeyForFailedScrapping +=1

        nhsDict[medName] = { "url" : href}

#sanity check
# for name,data in list(nhsDict.items())[:5]:
#     print("{} {}".format(name,data["url"]))

for name,url in list(nhsDict.items()):
    fixedUrl = url["url"]
    try:
        response = requests.get(fixedUrl)
        response.raise_for_status() #errors out if page down
        individualHTML = response.text
        medicineSoup = BeautifulSoup(individualHTML,'html.parser')
        
        summaryForMedicine = medicineSoup.find("p",class_="nhsuk-lede-text")
        if(summaryForMedicine):
            summaryForMedicineText = summaryForMedicine.get_text(strip = True)
        else:
            summaryForMedicineText = ""

        #Dictonary of Dictonaries
        nhsDict[name]["summary"] = summaryForMedicineText 
        time.sleep(.1) #politness slower scrapping
    except:
        print("Failed to scrape {}".format(fixedUrl))

#Sanity Check two
# for med,data in nhsDict.items():
#     print("{med}: {data['url']}\n{data['summary']}")

jsonStringToWrite = json.dumps(nhsDict,indent=4,sort_keys=True,ensure_ascii=False)

with open("SheerHealthFinalJSON.txt","w", encoding="utf-8") as f:
    f.write(jsonStringToWrite)