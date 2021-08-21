#!/bin/bash

#
# GET
#

#wgets -O 'um-sayounara-boku-no-majo.pdf' 'https://www.japancenter.cz/upload/files/downloads/um-sayounara-boku-no-majo.pdf'

#
# EXTRACT
#

#pdfimages um-sayounara-boku-no-majo.pdf majo

#
# SPLIT
#

#INDEX=0

#mkdir split/ 2>/dev/null

#for PAGE in {000..039}; do
#	convert -crop 100%x50% "majo-$PAGE.pbm" "out_%d.pbm"
#	mv "out_0.pbm" "split/majo-$INDEX.pbm"
#	((INDEX++))
#	mv "out_1.pbm" "split/majo-$INDEX.pbm"
#	((INDEX++))
#done

#
# ROTATE
#

# halves by 180... for left to right read..

#
# JOIN
#

#     PAGE: 0 3 2 5 4 7 6 9 8 .. 1
#    PRINT: 0 2 | 3 5 - 4 6 | 7 9 - 8 10 | 11 13 - .. 

INDEX=0
PAGE=0

mkdir merge/ 2>/dev/null

#mv "split/majo-1.pbm" "split/majo-81.pbm" 2>/dev/null #fix back cover..

for ((i=0;i < 20;i++)) do
	convert -append "split/majo-$INDEX.pbm" "split/majo-$(($INDEX + 2)).pbm" "merge/majo-$(printf '%03d' $PAGE).pbm";
	((PAGE++))
	convert -append "split/majo-$(($INDEX + 3)).pbm" "split/majo-$(($INDEX + 5)).pbm" "merge/majo-$(printf '%03d' $PAGE).pbm"; 
	INDEX=$(($INDEX + 4))
	((PAGE++))
done

#
# BACK
#

#convert -limit thread 2 "merge/majo*.pbm" fixed.pdf

