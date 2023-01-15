#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Scrap japanesetest4you.com from Wayaback
#
# A4: 595 x 842 PT
#

import StringIO,requests,lxml.html,json,time,sys,re

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# VAR

NAME='N3_Vocabulary.pdf'
URL='https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n3-vocabulary-exercise-'
API='https://archive.org/wayback/available'

PAGE=22

# MAIN

def download():

	session = requests.Session()

	for page in range(1, PAGE + 1):

		if page == 2: page = '2-2'# N3 vocabulary fix URL

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
			print('[*] API request failed')
			continue
		if not wayback:
			print('[*] API request empty set')
			continue

		print('[*] Wayback request')
		req = session.get(wayback)
		print('[*] Writing page')

		with open(str(page) + '.html', 'wb') as f: f.write(req.text.encode('utf-8'))

def get_pdf():

	pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))# 'HeiseiKakuGo-W5'
	pdf = Canvas(NAME, pagesize=A4)
	pdf.setFont('HeiseiMin-W3', 10)# 16
	pdf.setLineWidth(0.5)

	offset_top = 822
	offset_line = 11

	for page in range(1, PAGE + 1):

		try:
			f = open(str(page) + '.html', 'r')
		except:
			continue

		p = lxml.html.HTMLParser()
		t = lxml.html.parse(f, p)

		# GRAMMAR
		#data = t.xpath(".//div[@class='entry clearfix']//p")
		#for i in range(0,len(data)):
		#	val = data[i].xpath("text()")# raw text
		#	# Questions
		#	if len(data[i].xpath(".//input")) == 4:# has answers
		#		clean = [x.strip() for x in val if x != '\n'] #clean values
		#		pdf.drawString(offset_line,offset_top, ''.join(clean[:-4]))# multi-question not last 4
		#		offset_top -= 15
		#		for line in clean[-4:]:# last four
		#			pdf.drawString(offset_line, offset_top, str(clean.index(line)) + u'. ' + line)
		#			offset_top -= 15
		#		offset_top -= 5
		#		offset_line = 10
		#	# Answer
		#	if 'Question' in ''.join(val):
		#		answer = re.sub('Question [1]?[0-9]:', '', ''.join(val).strip().replace('\n',''))
		#		pdf.drawString(offset_line+250, offset_top, answer)

		# VOCABULARY

		QUESTION=1

		data = t.xpath(".//div[@class='entry clearfix']//p")
		for i in range(0,len(data)):
			val = data[i].xpath("text()")# raw text
			# Questions
			if len(data[i].xpath(".//input")) == 4:# has answers
				clean = [x.strip() for x in val if x != '\n'] #clean values
				try:
					question = data[i].xpath(".//span//text()")[0]
					pdf.drawString(offset_line,offset_top, str(QUESTION) + '. ' + question)# special text
					QUESTION+=1
				except:
					pdf.drawString(offset_line,offset_top, ''.join(clean[:-4]))# multi-question not last 4
				offset_top -= 17
				offset_line = 20
				for line in clean[-4:]:# last four
					pdf.drawString(offset_line, offset_top, str(clean.index(line)) + u'. ' + line)
					offset_line += 10*(2 + len(line))
			
				offset_top -= 17
				offset_line = 10 # reset
			# Answer
			if 'Question' in ''.join(val):
				answer = re.sub('Question [1]?[0-9]:', '', ''.join(val).strip().replace('\n',''))
				pdf.drawString(offset_line+250, offset_top, answer)
				offset_top -= 30

		#pdf.showPage()
		#offset_top = 822 #842
		#break

	pdf.save()

get_pdf()

