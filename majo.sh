#!/bin/bash

# get source
#wgets -O 'um-sayounara-boku-no-majo.pdf' 'https://www.japancenter.cz/upload/files/downloads/um-sayounara-boku-no-majo.pdf'

# extract images
#pdfimages um-sayounara-boku-no-majo.pdf majo

# split images
mkdir split/ 2>/dev/null
INDEX=0
for PAGE in {000..039}; do
	convert -crop 100%x50% "majo-$PAGE.pbm" "out_%d.pbm"
	mv "out_0.pbm" "split/majo-$INDEX.pbm"
	((INDEX++))
	mv "out_1.pbm" "split/majo-$INDEX.pbm"
	((INDEX++))
done

# join image

# image to pdf
#convert majo*.pbm test.pdf

# join PDF
