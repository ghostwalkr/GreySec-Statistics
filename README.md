# GreySec-Statistics
Statistics for greysec.net forum

![GS Scraper](https://imgur.com/vwCv9om "GS Scraper")
## Summary
This repo is for the GreySec Forums data scraper and some of the gathered data. The scraper gets the username, UID, post count, and thread count of a specified number of users.

## Installation
(scraper tested on Debian Buster)

Python: Beautiful Soup library (bs4)

`$ pip3 install bs4`

## Usage
Open scraper.conf file. This controls the behavior of the script.
 
* uid_start - The user ID to start with. Must be an integer higher than 0.
* uid_end - The user ID to end on. Must be an integer higher than 0.
* outfile - The file to write output to. Output is JSON format. Must be relative or full path to a file. If the file exists it is overwritten.
* verbose - Verbose output shows the progress of the script. It also shows the data being gathered on each profile. Can be either true or false. Case sensitive.

To run: `$ python3 scraper.py` or...
 
 `$ chmod 700 scraper.py && ./scraper.py`
 
 ## Output
```
 {
	"starttime": "9-9_2020-6-2",
	"endtime": "10-7_2020-6-2",
	"data": {
		"1": {
			"username": "Insider",
			"postcount": "1070",
			"threadcount": "277"
		},
		"2": {
 ```
 ### To do
 * Make the HTTP requests threaded.
 * Have some way for user to choose how they want to handle errors. For example, if the script fails to get a profile user could choose between having the script continue or just stop execution altogether.
