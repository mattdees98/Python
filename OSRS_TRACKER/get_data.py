# import statements
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import time
import csv
from bs4 import BeautifulSoup

# open and read json file for item IDs
f = open('osrs_items.json')
data = json.load(f)

# open csv file and initialize writer
data_file = open('item_data.csv', 'w')
csv_writer = csv.writer(data_file)

# flatten JSON hierarchies
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# iterate through item IDs and request JSON information from OSRS item sites
for item in data:
		
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	struct = {}
	url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(item['id'])
	response = requests.get(url)

	# if we receive a JSON response then continue
	if (response.status_code == 200):
		r = response.json()
		r = flatten_json(r)

		# write JSON strings from web scraping to single file
		with open('data.json', 'a') as outfile:
			json.dump(r, outfile, ensure_ascii = False, indent = 4)
			print('Record added to data.json: ', item['id'])

		# print raw JSON string
		#print(json.dumps(r, indent = 4, sort_keys = True))
	else:
		print("404 ERROR - NO JSON RESPONSE")
		r = 'error'

	# sleep for 4 seconds in between requests
	time.sleep(10)

# close data file
data_file.close()


