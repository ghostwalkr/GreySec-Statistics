#!/usr/bin/env python3
import sys, json, re, requests
from bs4 import BeautifulSoup

logfile = "greysec-scraper.log"
datafile = "greysec-data.json"

def parse_data(data):
    # data - BeautifulSoup object to scrape <bs4>
    postcount = "NULL"
    threadcount = "NULL"
    # Find username
    username = re.search("of [\S' ']{3,30}$", data.title.text).group().replace("of ","").strip()

    # Find post count
    for trow in data.find_all(class_="trow1"):
        if "posts per" in trow.text:
            postcount = re.search("^\d{1,10}", trow.text.replace(",","")).group().strip()
            break

    # Find thread count
    for trow in data.find_all(class_="trow2"):
        if "threads per" in trow.text:
            threadcount = re.search("^\d{1,10}", trow.text.replace(",","")).group().strip()
    
    userdata = {
            "username":f"{username}",
            "postcount":f"{postcount}",
            "threadcount":f"{threadcount}"
            }

    return userdata

headers = {
        "User-Agent":"Greysec-Scraper-v1.2",
        "Cookie":"mybb[lastvisit]=1589776861; mybb[lastactive]=1589776872; loginattempts=1; mybbuser=7904_ILJLmsD0wfnoPt5TfwbTd2nd4ghja0YvfQsa9jN3G5rpCWzZAH; sid=c89900f45635fdff3a2206082b19aa4b"
        }

allusers = {}

for user in range(913,8170):
    uid = str(user)
    
    print(f"[*] Getting data on uid {uid}")
    try:
        html = BeautifulSoup(requests.get(f"https://greysec.net/member.php?action=profile&uid={user}", headers=headers).text, "html.parser")
    except Exception as error:
        with open(logfile, "a") as log:
            log.write(error + "\n")
            log.close()
        continue

    data = json.dumps(parse_data(html))

    with open(datafile, "a") as outfile:
        outfile.write(f'"{uid}":{data},\n')
        outfile.close()

    print(data + "\n")
