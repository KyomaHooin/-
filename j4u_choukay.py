#!/usr/bin/python

import StringIO,requests,lxml.html,time,sys,re

API='https://archive.org/wayback/available'
URL='https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n3-listening-exercise-'
PAGE=22

session = requests.Session()
session.headers.update({'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'})

for page in range(1, PAGE + 1):

	print('[*] Page ' + str(page))
	
	time.sleep(5)

	print('[*] API request')

	wayback = None;
	req = session.post(API, data={'url': URL + str(page)})

	if req.status_code == 200:
		res = req.json()
		if res['results'][0]['archived_snapshots']:
			wayback = res['results'][0]['archived_snapshots']['closest']['url']
	else:
		print('[*] API request failed.')
		continue
	
	if not wayback:
                print('[*] API request empty set.')
                continue

	time.sleep(5)

	print('[*] Wayaback request')
	req = session.get(wayback)
	
	p = lxml.html.HTMLParser()
	t = lxml.html.parse(StringIO.StringIO(req.text), p)

	data = t.xpath(".//audio/a/@href")
	if not data: data = t.xpath('.//audio/@src')

	for mp3 in data:
		name = re.sub('.*/','', mp3)
		url = re.sub('.*(https.*)','\\1', mp3)

		time.sleep(5)

		req = session.get(url)
		print('[*] Writing ' + name)
		with open(re.sub('.*/','', mp3), 'wb') as f: f.write(req.content)

session.close()

