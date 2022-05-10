#!/usr/bin/python

import StringIO,requests,lxml.html,sys,re

URL='https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n4-listening-exercise-'

session = requests.Session()
session.headers.update({'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'})

PAGE=55

for page in range(1,PAGE):

	req = session.get(URL + str(page))

	p = lxml.html.HTMLParser()
	t = lxml.html.parse(StringIO.StringIO(req.text), p)

	data = t.xpath(".//audio//a")

	for a in data:
		mp3 = a.get("href")
		name = re.sub('.*/','', mp3)
		req = session.get(mp3)
		print("Writing " + name + ' ..' )
		with open(re.sub('.*/','', mp3), 'wb') as f: f.write(req.content)

session.close()
		
