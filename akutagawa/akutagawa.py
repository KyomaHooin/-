#!/usr/bin/python3
#
# Search japan.cz library for Akutagawa winner
#

import requests,lxml.html,time,sys
from urllib.parse import quote
from io import StringIO

URL='https://www.librarycat.org/lib/ceskojaponska/search/text/'
AKUTAGAWA='akutagawa.txt'

session = requests.Session()

with open(AKUTAGAWA,'r') as f:
	for name in f:
		print(name.strip(), end='', flush=True)
		req = session.get(URL + name.strip())
		p = lxml.html.HTMLParser()
		t = lxml.html.parse(StringIO(req.text), p)
		if req.status_code == 200:
			data = t.xpath('//div[@id="resultsbox"]/div/div/text()')
			if not 'No results found.' in data:
				print(" !")
			else:
				print()
		time.sleep(5)
