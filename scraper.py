import sys, json, re, requests, configparser
from bs4 import BeautifulSoup
from time import localtime, ctime, sleep
from pprint import pprint

headers = {
        "User-Agent":"Greysec-Scraper-v1.2",
        "Cookie":""
        }
now = localtime()
start_time = "{}-{}_{}-{}-{}".format(now.tm_hour, now.tm_min, now.tm_year, now.tm_mon, now.tm_mday)

def banner():
    print("""                #################
              #######################
            #####*######################
          ###############################
         ###################r#############
        ###################################
        ###################################
        ###           #######           ###
        #              #####              #
        #              #####              #
        ##            #######            ##
        ####        ###########        ####
        ###################################
          ##############   ##p###########
        ######$########     ###############
        #  ############################# ##
        ## #############00############# ###
        #############################  ####
         ####  ## ###   #### #### ## ##### 
          ##### ######## ### #  ## # ####  
           #### ###  #  #### ### #######
            ########## #  ### ## ######
             #################    # ##
                ##################
                 ################

             GreySec Data Scraper v1.3""")
    sleep(2)

def get_profile(uid=None):
    if uid == None:
        print("Error: function get_profile uid parameter not set")
        return False
    try:
        profile = BeautifulSoup(requests.get(f"https://greysec.net/member.php?action=profile&uid={uid}", headers=headers).text, "html.parser")
    except Exception as error:
        print(f"Exception in function get_profile: {error}")
        return False

    return profile

def parse_data(data):
    # data - BeautifulSoup object to scrape <bs4>
    username = "NULL"
    postcount = "NULL"
    threadcount = "NULL"
    # Find username
    try:
        username = re.search("of [\S' ']{3,30}$", data.title.text).group().replace("of ","").strip()
    except:
        username = "PARSING_ERROR"

    # Find post count
    for trow in data.find_all(class_="trow1"):
        if "posts per" in trow.text:
            try:
                postcount = re.search("^\d{1,10}", trow.text.replace(",","")).group().strip()
            except:
                postcount = "PARSING_ERROR"

            break

    # Find thread count
    for trow in data.find_all(class_="trow2"):
        if "threads per" in trow.text:
            try:
                threadcount = re.search("^\d{1,10}", trow.text.replace(",","")).group().strip()
            except:
                threadcount = "PARSING_ERROR"
                
            break
    
    userdata = {
            "username":f"{username}",
            "postcount":f"{postcount}",
            "threadcount":f"{threadcount}"
            }

    return userdata

## Main ##
##########################

banner()

# Load configuration from file
try:
    config = configparser.ConfigParser()
    config.read("scraper.conf")
    user_range = [ int(config["MAIN"]["uid_start"]), int(config["MAIN"]["uid_end"]) ]
    version = "greysec_scraper_v1.3"
    datafile = config["MAIN"]["outfile"]
    verbose = config["MAIN"]["verbose"]
except Exception as error:
    print(f"Error: {error}")
    sys.exit(1)

print("Starting GreySec Data Scraper at {}".format(ctime()))

data_output = {
        "starttime": start_time,
        "endtime": "ENDTIME",
        "data": {}
        }
try:
    for user in range(user_range[0],user_range[1] + 1):
        uid = str(user)
    
        if verbose == "true":
            print(f"[*] Getting data on uid {uid}")

        html = get_profile(uid)
        if html == False: # If an error occurred in the get_profile function
            continue
    
        data_output["data"][uid] = parse_data(html)
#    data = json.dumps(parse_data(html))

#    with open(datafile, "a") as outfile:
#        outfile.write(f'"{uid}":{data},\n')
#        outfile.close()
        if verbose == "true":
            print(str(data_output["data"][uid]) + "\n")

    end_time = "{}-{}_{}-{}-{}".format(localtime().tm_hour, localtime().tm_min, localtime().tm_year, localtime().tm_mon, localtime().tm_mday)
    data_output["endtime"] = end_time

except KeyboardInterrupt:
    print("\nUser interrupt. Finishing up...")

finally:
    # Write results to file

    with open(datafile, "w") as out:
        json.dump(data_output, out, indent="\t")
        out.close()

    print("GreySec Data Scraper Complete at {}".format(ctime()))
