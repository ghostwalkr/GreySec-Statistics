#!/usr/bin/env python3
import sys, json, re, requests
from bs4 import BeautifulSoup

logfile = "greysec-scraper.log"
datafile = "greysec-data.json"

def parse_data(data):
    # Parses a beautiful soup object. The bs object should be the html of a GreySec User profile. Returns a dictionary of the username, post count, and thread count.
    # data - BeautifulSoup object to scrape <bs4>
    postcount = "NULL"
    threadcount = "NULL"
    # Find username
    # Regex parses the html title, gets the section of text after "of ", which should be the username.
    username = re.search("of [\S' ']{3,30}$", data.title.text).group().replace("of ","").strip()

    # Find post count
    for trow in data.find_all(class_="trow1"):
        if "posts per" in trow.text:
            postcount = re.search("^\d{1,10}", trow.text.replace(",","")).group().strip()
            break

    # Find thread count
    for trow in data.find_all(class_="trow2"):
        # Looping through every tag with a trow2 class isn't efficient. Need to find a better way to parse the post count and thread count.
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
        "Cookie":"Insert your GreySec Cookie here"
        }

allusers = {}

for user in range(1,8170): # Greysec users as of time of writing: 8,169. 
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
