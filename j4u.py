#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Scrap japanesetest4you.com ..
#
# A4: 595 x 842 PT
#

import StringIO,requests,lxml.html,sys,re

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# VAR

#NAME='N4_Grammar.pdf'
#URL='https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n4-grammar-exercise-'
#PAGE=31
NAME='N4_Vocabulary.pdf'
URL='https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n4-vocabulary-exercise-'
PAGE=32

# SETUP

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))# 'HeiseiKakuGo-W5'
pdf = Canvas(NAME, pagesize=A4)

# MAIN

session = requests.Session()
session.headers.update({'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'})

for page in range(1,PAGE):
	
	#if page in [18,19,20]: continue# grammar skip JLPT5 ;)
	if page == 8: page = '08'# vocabulary fix URL
	if page == 9: page = '09'# vocabulary fix URL

	print("Scrapping test: " + str(page))

	offset_top = 822 #842
	offset_line = 10

	pdf.setFont('HeiseiMin-W3', 10)# 16
	pdf.setLineWidth(0.5)

	req = session.get(URL + str(page))

	if req and req.status_code == 200:

		p = lxml.html.HTMLParser()
		t = lxml.html.parse(StringIO.StringIO(req.text), p)

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
				offset_top -= 15
				for line in clean[-4:]:# last four
					pdf.drawString(offset_line, offset_top, str(clean.index(line)) + u'. ' + line)
					offset_top -= 15
				offset_top -= 5
				offset_line = 10
			# Answer
			if 'Question' in ''.join(val):
				answer = re.sub('Question [1]?[0-9]:', '', ''.join(val).strip().replace('\n',''))
				pdf.drawString(offset_line+250, offset_top, answer)

	# write page		
	pdf.showPage()

# write PDF
pdf.save()

# EXIT

sys.exit(0)

