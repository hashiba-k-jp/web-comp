import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

URL = "https://www.data.jma.go.jp/developer/xml/feed/extra_l.xml"

# This should NOT be fixed ... but not enough time.
TARGET_REGION = "仙台管区気象台"

def search(region):
    # get info from JMA server
    response = requests.get(URL)
    response.encoding = response.apparent_encoding
    # print(response.text)
    soup = bs(response.content, 'xml')

    # get detail data
    entries = soup.find_all('entry')
    targets = [e for e in entries if e.find('name').string==region]
    # print(targets)

    # select newest one
    # This should be stored to DB, but not enough time ...
    for target in targets:
        update_time = target.find('updated').string
        print(update_time)
        dt3 = datetime(
            year=int(date[0:4]),month=int(date[5:7]),day=int(date[8:10]),
            hour=int(date[11:13]),minute=int(date[14:16]),second=int(date[17:20])
        )



if __name__=="__main__":
    search(TARGET_REGION)
