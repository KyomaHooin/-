#!/bin/bash

#
# GET
#

wget -O 'um-sayounara-boku-no-majo.pdf' 'https://www.japancenter.cz/upload/files/downloads/um-sayounara-boku-no-majo.pdf'

#
# EXTRACT
#

pdfimages um-sayounara-boku-no-majo.pdf majo

#
# SPLIT
#

mkdir split/ 2>/dev/null

INDEX=0

for PAGE in {000..039}; do
	convert -crop 100%x50% "majo-$PAGE.pbm" "out_%d.pbm"
	mv "out_0.pbm" "split/majo-$INDEX.pbm"
	((INDEX++))
	mv "out_1.pbm" "split/majo-$INDEX.pbm"
	((INDEX++))
done

#
# JOIN
#

#  PAGE: 0 3 2 5 4 7 6 9 8 .. 1
# PRINT: 0 81 | 3 78 - 2 79 | 5 76 - 4 77 | 7 74 - .. 

mkdir merge/ 2>/dev/null

mv "split/majo-1.pbm" "split/majo-81.pbm" 2>/dev/null #fix back cover..

FIRST=0
LAST=81
PAGE=0

for ((i=0;i < 20;i++)) do

	convert -append "split/majo-$FIRST.pbm" "split/majo-$LAST.pbm" "merge/majo-$(printf '%03d' $PAGE).pbm";
	((PAGE++))

	mogrify -rotate 180 "split/majo-$(($FIRST + 3)).pbm"
	mogrify -rotate 180 "split/majo-$(($LAST - 3)).pbm"

	convert -append "split/majo-$(($FIRST + 3)).pbm" "split/majo-$(($LAST - 3)).pbm" "merge/majo-$(printf '%03d' $PAGE).pbm"; 
	((PAGE++))

	FIRST=$(($FIRST + 2))
	LAST=$(($LAST - 2))
done

#
# BACK
#

convert -limit thread 2 "merge/majo*.pbm" fixed.pdf

