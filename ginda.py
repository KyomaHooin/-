#!/usr/bin/python3
#
# Sakura HTML to PDF
#

import lxml.html

from io import BytesIO

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

OFFSET_TOP=0
OFFEST_LINE=0

###########################
#INIT
###########################

#canvas
#pdf = Canvas(PDF, pagesize=pagesizes.landscape(pagesizes.A4))
# title
#pdf.setTitle(TITLE)
# register font
#pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3','90ms-RKSJ-V'))# Vetical HeiseiMin-W3

###########################
# MAIN
###########################

with open(FILE,'r') as f:

	# HTML parse
	p = lxml.html.HTMLParser()
	data = lxml.html.parse(f, p)

	for el in data.xpath('./body/*'):
		#
		# logo..		ZeroDrop _pageBreakAfterAlways 
		# image ..		FloatCenterImage
		# footer ..		creditsdiv
		# header..		SmallHeader
		# text..		AlignBottom
		# text..		FiveDrop
		# text..		OneDrop
		# text or break ..	ZeroDrop
		#

		print(el.get('class'))

	# Gen. data
	#pdf.setFont('HeiseiMin-W3', 16) # 16x16
	#pdf.drawString(50,550,"銀田の事件簿")

	#pdf.setFont('HeiseiMin-W3', 8)# 8x8
	#pdf.drawString(65,550,'ぎん')
	#pdf.drawString(65,530,'だ')

	#pdf.drawImage(ImageReader(img),70,50,700,470)

	# write page
	#pdf.showPage()
	#pdf.save()

