#!/usr/bin/python3
#
# Sakura HTML to PDF
#

import lxml.html

from io import BytesIO

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes
from reportlab.lib.utils import ImageReader

#INIT

pdf = Canvas('out.pdf', pagesize=pagesizes.landscape(pagesizes.A4))

pdf.setTitle("日本")
pdf.setFont('Helvetica', 10)
pdf.drawString(50,550,"日本")
pdf.line(50,545,790,543)
#pdf.drawImage(ImageReader(img),70,50,700,470)
pdf.line(50,45,790,43)
pdf.showPage()
pdf.save()
