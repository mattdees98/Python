import requests
import sys
import json
import sqlite3
import urllib.request
import time
import re
from bs4 import BeautifulSoup

f = open('osrs_items.json')
data = json.load(f)

db = sqlite3.connect('C:\sqlite\item_db')
cursor = db.cursor()
#cursor.execute("DROP TABLE IF EXISTS items")
#cursor.execute("CREATE TABLE items (id int, name text, price double, alch double)")

for item in data:
	
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	struct = {}
	url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(item['id'])
	response = requests.get(url)

	if (response.status_code == 200):
		r = response.json()
		item_id = r['item']['id']
		print('ID: ', item_id)
		item_name = r['item']['name']
		print('Name: ', item_name)
		item_price = r['item']['current']['price']
		print('Price: ', item_price)
		print(' ')
		time.sleep(5)
		#print(json.dumps(r, indent = 4, sort_keys = True))
	else:
		print("Error. Not in JSON format")
		r = 'error'
	

