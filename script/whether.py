import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from datetime import timedelta
import unicodedata
import pprint as pp
import send

URL = "https://www.data.jma.go.jp/developer/xml/feed/extra_l.xml"
TIMESPAN = 30

# This should NOT be fixed ...
TARGET_REGION = "仙台管区気象台"

def search(region, check_time):
    send_date = []

    # get info from JMA server
    response = requests.get(URL)
    response.encoding = response.apparent_encoding
    # print(response.text)
    soup = bs(response.content, 'xml')

    # get detail data
    entries = soup.find_all('entry')
    targets_region = [e for e in entries if e.find('name').string==region]
    targets = [t for t in targets_region if t.find('title').string=="府県気象情報"]
    # print(targets)

    for target in targets:
        update_time = target.find('updated').string
        # print(update_time)
        issued_time = datetime(
            year=int(update_time[0:4]),month=int(update_time[5:7]),day=int(update_time[8:10]),
            hour=int(update_time[11:13]),minute=int(update_time[14:16]),second=int(update_time[17:19])
        ) + timedelta(hours=9)
        print(issued_time, issued_time > check_time)

        if issued_time > check_time:
            # send message here !
            content = target.find('content').string
            content = content.replace('】', '】\n')
            split = content.split('\n')
            if len(split) == 2:
                title = unicodedata.normalize('NFKC', split[0])
                body = unicodedata.normalize('NFKC', split[1])
                content = None
                split_ed = True
            else:
                title = None
                body = None
                content = unicodedata.normalize('NFKC', content)
                split_ed = False

            date = f"{issued_time.year:04}/{issued_time.month:02}/{issued_time.day:02} {issued_time.hour:02}:{issued_time.minute:02}"
            send_date.append(
                {
                    "date":date,
                    "region":region,
                    "title":title,
                    "body":body,
                    "content":content,
                    "split_ed":split_ed
                }
            )
        else:
            pass

    return send_date


def main():
    # This program is estimeted to be run in each 30 minutes.
    dt_now = datetime.now()
    dt_now = datetime(2023, 7, 19, 5, 30, 0) # This is a sample datetime

    check_time = dt_now - timedelta(
        minutes = (dt_now.minute % TIMESPAN) + TIMESPAN,
        seconds = dt_now.second,
        microseconds = dt_now.microsecond
    )
    # If TIMESPAN = 30: This is the shortest time, from 30 to 59 minutes.
        # for exsample, 14:30 will be 14:00 ; send data issued after 14:00
        # for exsample, 06:01 will be 05:30 ; send data issued after 05:00
    print(check_time)

    res = search(
        region = TARGET_REGION,
        check_time = check_time
    )

    for content in res:
        if content["split_ed"]:
            text = f'{content["title"]}\n{content["date"]}\n{content["body"]}\n{content["region"]}'
        else:
            text = content["content"]
        #print(text)
        send.send_msg(text)
    # pp.pprint(tmp)

if __name__=="__main__":
    main()
