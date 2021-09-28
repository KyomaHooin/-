#!/usr/bin/python3
#
# Sakura HTML to PDF
#
# A4 landscape: 0-
#
# TODO: Delete copyright data from Git history.
#

import lxml.html,sys,re

#from io import BytesIO

# PDF Canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes
from reportlab.lib.utils import ImageReader

# Kanji / Kana
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

###########################
# VAR
###########################
#

FILE='sakura/ginda.html'
DATA='sakura/ginda_data'
PDF='ginda.pdf'

TITLE='銀田の事件簿'

OFFSET_BOTTOM=0
OFFSET_LEFT=0

###########################
#INIT
###########################

#canvas
pdf = Canvas(PDF, pagesize=pagesizes.landscape(pagesizes.A4))
# title
pdf.setTitle(TITLE)
# register font
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3','90ms-RKSJ-V'))# Vetical HeiseiMin-W3

###########################
# MAIN
###########################

with open(FILE,'r') as f:

	# HTML parse
	p = lxml.html.HTMLParser()
	data = lxml.html.parse(f, p)

	for el in data.xpath('./body/*'):
		#print(el.get('class'))
		#
		# IMAGE
		#
		# logo..		ZeroDrop _pageBreakAfterAlways 
		# image ..		FloatCenterImage
		# footer ..		creditsdiv
		#
		# TEXT
		#
		# header..		SmallHeader
		# text bottom		AlignBottom
		
		# text..		FiveDrop
		# text..		OneDrop
		# text or break ..	ZeroDrop
		#

		# LOGO
		#if el.get('class') == 'ZeroDrop _pageBreakAfterAlways':
		#	img_path = DATA + '/' + re.sub('.*\/','', el.xpath('./img/@src')[0])
		#	pdf.drawImage(ImageReader(img_path),0,0,600,600)

		# HEADER
		#if el.get('class') == 'header':
		# TEXT
		if el.get('class') in ['ZeroDrop','OneDrop','FiveDrop']:
			# break
			if len(el.xpath('./br')) > 0:
				OFFSET_LEFT-=16
			else:
				rs = 
				for text in el.itertext():# all text
					# if not a ruby => print
					# if ruby => skipt index by 2 + print furigana	

				OFFSET_LEFT-=16
		
		#pdf.setFont('HeiseiMin-W3', 16) # 16x16
		#pdf.drawString(50,550,"銀田の事件簿")

		#pdf.setFont('HeiseiMin-W3', 8)# 8x8
		#pdf.drawString(65,550,'ぎん')
		#pdf.drawString(65,530,'だ')

		#pdf.drawImage(ImageReader(img),70,50,700,470)

		# write page
	pdf.showPage()
	# write PDF
	pdf.save()

