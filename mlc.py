#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Scrap mlcjapanese.co.jp ..
#
# A4: 595 x 842 PT
#

import StringIO,requests,lxml.html,sys,re

from lxml.etree import tostring

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# VAR

NAME='N4_Grammar_MLC.pdf'
URL='https://www.mlcjapanese.co.jp/n4_jlpt_grammar_quiz_'
PAGE=13

# SETUP

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))# 'HeiseiKakuGo-W5'
pdf = Canvas(NAME, pagesize=A4)

# MAIN

session = requests.Session()
session.headers.update({'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'})

for page in range(1,PAGE):

	print("Scrapping test: " + str(page))

	offset_top = 822 #842
	offset_line = 10

	pdf.setFont('HeiseiMin-W3', 10)# 16
	pdf.setLineWidth(0.5)

	req = session.get(URL + str(page).zfill(2) + '.html')

	if req and req.status_code == 200:
	
		req.encoding = 'UTF-8'# force encoding

		p = lxml.html.HTMLParser()
		t = lxml.html.parse(StringIO.StringIO(req.text), p)

		# GRAMMAR

		data = t.xpath(".//div[@class='sp-part-top sp-html-src']")[4:]
	
		for i in range(0,len(data)):
			question = data[i].text_content().splitlines()[0]
			pdf.drawString(offset_line,offset_top, question)
			offset_top -= 15
			for line in data[i].text_content().splitlines()[2:-1]:# skip first and last rubbish
				pdf.drawString(offset_line,offset_top, line)
				offset_top -= 15
	# write page		
	pdf.showPage()

# write PDF
pdf.save()

# EXIT

sys.exit(0)

