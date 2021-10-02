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

###########################
# VAR
###########################

FILE='sakura/ginda.html'
DATA='sakura/ginda_data'
PDF='ginda.pdf'

TITLE='銀田の事件簿'

###########################
#INIT
###########################

#canvas
pdf = Canvas(PDF, pagesize=pagesizes.A5)
# title
pdf.setTitle(TITLE)
# register font
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3','90ms-RKSJ-V'))# Vetical HeiseiMin-W3

###########################
# MAIN
###########################

OFFSET_TOP=560
OFFSET_LEFT=380

with open(FILE,'r') as f:

	p = lxml.html.HTMLParser()
	data = lxml.html.parse(f, p)

	PAGE=1

	# LOGO
	# ratio: 1.333125
	pdf.drawImage('sakura/ginda_data/1-1.jpg', 0, 0, 400, 400*1.333125)
	pdf.showPage()

	# BLANK
	pdf.showPage()

	for el in data.xpath('./body/*'):

		# TEXT
		if el.get('class') in ['SmallHeader','ZeroDrop','OneDrop','FiveDrop','AlignBottom']:
			# break
			if len(el.xpath('./br')) > 0: continue
			# all text
			text = [t for t in el.itertext()]
			# header
			if el.get('class') == 'SmallHeader': text = ['■'] + text + ['■']
			# all ruby
			ruby = el.xpath('./ruby/text()')
			FURIGANA=False
			LEN=0
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
pdf.showPage()
# FOOT
# ratio: 1,037667072
pdf.drawImage('sakura/ginda_data/colo.jpg', 60, 150, 300*1.037667072, 300) 
pdf.showPage()

# write PDF
pdf.save()

