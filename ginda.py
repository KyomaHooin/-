#!/usr/bin/python3
#
# Sakura HTML to PDF
#
# A4 landscape: 0-
#
# TODO: Delete copyright data from Git history.
#

import lxml.html,sys,re
# PDF Canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes
from reportlab.lib.utils import ImageReader
# Kanji / Kana
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
# Formating
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph,Frame

###########################
# VAR
###########################

FILE='sakura/ginda.html'
DATA='sakura/ginda_data'
PDF='ginda.pdf'

TITLE='銀田の事件簿'

# 560x800
OFFSET_TOP=560
OFFSET_LEFT=400+400

###########################
#INIT
###########################

#canvas
pdf = Canvas(PDF, pagesize=pagesizes.landscape(pagesizes.A4))
# title
pdf.setTitle(TITLE)
# register font
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3','90ms-RKSJ-V'))# Vetical HeiseiMin-W3
# create A5 frame
frame1 = Frame(20,  20, 380, 555, showBoundary=1)
frame2 = Frame(440, 20, 380, 555, showBoundary=1)
#frame1.drawBoundary(pdf)
#frame2.drawBoundary(pdf)
# paragraph style
styles = getSampleStyleSheet()
style = styles['Normal']
# text buffer
story = []

###########################
# MAIN
###########################

with open(FILE,'r') as f:

	p = lxml.html.HTMLParser()
	data = lxml.html.parse(f, p)

	for el in data.xpath('./body/*'):
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
		#
		# LOGO
		#if el.get('class') == 'ZeroDrop _pageBreakAfterAlways':
		#	img_path = DATA + '/' + re.sub('.*\/','', el.xpath('./img/@src')[0])
		#	pdf.drawImage(ImageReader(img_path),0,0,600,600)
		# HEADER
		#if el.get('class') == 'header':

		break

		# TEXT
		if el.get('class') in ['ZeroDrop','OneDrop','FiveDrop']:
			# break
			if len(el.xpath('./br')) > 0:
				OFFSET_LEFT-=16
			else:
				# text
				text = [t for t in el.itertext()]
				# ruby
				ruby = el.xpath('./ruby/text()')
				# loop
				FURI=False
				for i in range(0,len(text)):
					# text break
					if OFFSET_TOP < 100:
						OFFSET_LEFT-=2*16
						OFFSET_TOP=560
					# skip furigana
					if FURI:
						FURI=False
						continue
					if text[i] not in ruby:
						pdf.setFont('HeiseiMin-W3', 16)
						#pdf.drawString(OFFSET_LEFT, OFFSET_TOP, text[i])
						#story.append(Parahraphtext[i])
						# offset
						#OFFSET_TOP-=16*len(text[i])
					else:
						pdf.setFont('HeiseiMin-W3', 16)
						pdf.drawString(OFFSET_LEFT, OFFSET_TOP, text[i])
						pdf.setFont('HeiseiMin-W3', 8)
						pdf.drawString(OFFSET_LEFT+16, OFFSET_TOP, text[i+1])
						# offset
						OFFSET_TOP-=16*len(text[i])
						# furigana
						FURI=True
				# line break
				OFFSET_LEFT-=2*16
				OFFSET_TOP=560
			# write page
			if OFFSET_LEFT < 20:
				pdf.showPage()
				OFFSET_LEFT=800
				OFFSET_TOP=560
				
	
		#pdf.drawImage(ImageReader(img),70,50,700,470)

		# write page
	pdf.showPage()
	# write PDF
	pdf.save()

