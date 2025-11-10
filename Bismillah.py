import requests
from bs4 import BeautifulSoup

nhsDict = {}

#requests to extract html and css from nhs hyperlink 
nhsMedicinePageListURL = "https://www.nhs.uk/medicines/" #constant
response = requests.get(nhsMedicinePageListURL)
nhsRawHTML = response.text
strNHSMedicineFileName = "nhsPageListRawHTMLText.txt"

try:
    with open(strNHSMedicineFileName,"w") as f:
        f.write(nhsRawHTML)
    print("Successful text scrapping and dumping\n")
except IOError as e:
    print("Error saving scrapped NHS main List page HTML Error is : {}".format(e))
    