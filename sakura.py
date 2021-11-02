#!/usr/bin/python3
#
# Sakura HTML to PDF
#
# TODO: Delete copyright data from Git history.
# TODO: scale image to A5 page centered
#
import lxml.html,sys,re
# PDF Canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes
from reportlab.lib.utils import Image,ImageReader
# Kanji / Kana
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
# Image
#from PIL import Image

###########################
# VAR
###########################

LIST=['kearo','oomisaka','suika','sennin','yakusoku','yume','yume2']

TITLE={
	'kearo':'蛙',
	'oomisaka':'大晦日の小さな事件',
	'suika':'不思議な老人と西瓜',
	'sennin':'仙人',
	'yakusoku':'守られた約束',
	'yume':'夢十夜」第一夜',
	'yume2':'夢十夜」第三夜'
}

DIR='sakura/'
PDF='sakura.pdf'

###########################
#INIT
###########################

#canvas
pdf = Canvas(PDF, pagesize=pagesizes.A5)
# title
pdf.setTitle('さくら多読ラボ')
# register font
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3','90ms-RKSJ-V'))# Vetical HeiseiMin-W3
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5','90ms-RKSJ-V'))# Vetical HeiseiMin-W3

###########################
# MAIN
###########################

for BOOK in LIST:

	OFFSET_TOP=560
	OFFSET_LEFT=380

	with open(DIR + BOOK + '.html','r') as f:

		p = lxml.html.HTMLParser()
		data = lxml.html.parse(f, p)

		PAGE=1

		# TITLE
		pdf.setFont('HeiseiKakuGo-W5', 36)
		pdf.drawString(210, 450, TITLE[BOOK])
		pdf.showPage()

		if BOOK == 'yume2':
			DATA = data.xpath('./body/div[@id="_idContainer001"]/p')
		else:
			DATA = data.xpath('./body/p')

		for el in DATA:
			# all text
			text = [t for t in el.itertext()]
			# all ruby
			ruby = el.xpath('./ruby/text()')
			FURIGANA=False
			# loop
			for i in range(0, len(text)):
				# furigana
				if FURIGANA:
					FURIGANA=False
					continue
				# hira/katakana
				if text[i] not in ruby:
					# kana char by char
					for kana in text[i]:
						# line wrap
						if OFFSET_TOP < 40:
							OFFSET_TOP=560
							OFFSET_LEFT-=2*16
							# page wrap
							if OFFSET_LEFT < 20:
								pdf.setFont('HeiseiMin-W3', 8)
								for i in range(0,len(str(PAGE))):
									pdf.drawString(195+i*8, 20, str(PAGE)[i])# page num.
								PAGE+=1
								pdf.showPage()
								OFFSET_TOP=560
								OFFSET_LEFT=380
						# write char
						pdf.setFont('HeiseiMin-W3', 16)
						pdf.drawString(OFFSET_LEFT, OFFSET_TOP, kana)
						OFFSET_TOP-=16
				# kanji
				else:
					#line wrap
					if OFFSET_TOP < 40:
						OFFSET_TOP=560
						OFFSET_LEFT-=2*16
						# page wrap
						if OFFSET_LEFT < 20:
							pdf.setFont('HeiseiMin-W3', 8)
							for i in range(0,len(str(PAGE))):
								pdf.drawString(195+i*8, 20, str(PAGE)[i])# page num.
							PAGE+=1
							pdf.showPage()
							OFFSET_TOP=560
							OFFSET_LEFT=380
					# kanji as set
					pdf.setFont('HeiseiMin-W3', 16)
					pdf.drawString(OFFSET_LEFT, OFFSET_TOP, text[i])
					# add furtigana
					pdf.setFont('HeiseiMin-W3', 8)
					#
					# furigana offset:
					#
					# a] get kanji center offset len
					# b] get furigana half len
					# c] substract
					#
					pdf.drawString(OFFSET_LEFT+16, OFFSET_TOP - 8*len(text[i]) + 4*len(text[i+1]) , text[i+1])
					OFFSET_TOP-=16*len(text[i])
					FURIGANA=True
	pdf.setFont('HeiseiMin-W3', 8)
	for i in range(0,len(str(PAGE))):
		pdf.drawString(195+i*8, 20, str(PAGE)[i])# page num.
	# write page
	pdf.showPage()
	# BLANK
	#pdf.showPage()

# write PDF
pdf.save()

