#!/bin/bash

#
# GET
#

wget -O 'um-sayounara-boku-no-majo.pdf' 'https://www.japancenter.cz/upload/files/downloads/um-sayounara-boku-no-majo.pdf'

#
# EXTRACT
#

echo -n "Extracting.. " 
pdfimages -png um-sayounara-boku-no-majo.pdf majo
echo "Done."

#
# SPLIT
#

INDEX=0

echo -n "Spliting.. " 
mkdir split/ 2>/dev/null
for PAGE in {000..039}; do
	convert -crop 100%x50% "majo-$PAGE.png" "out_%d.png"
	mv "out_0.png" "split/majo-$INDEX.png"
	((INDEX++))
	mv "out_1.png" "split/majo-$INDEX.png"
	((INDEX++))
done
echo "Done."

#
# JOIN
#
#  PAGE ORDER: 0 3 2 5 4 7 6 9 8 .. 1
# PRINT ORDER: 0 81 | 3 78 - 2 79 | 5 76 - 4 77 | 7 74 - .. 
#

FIRST=0
LAST=81
PAGE=0

echo -n "Joining.. " 
mkdir merge/ 2>/dev/null
mv "split/majo-1.png" "split/majo-81.png" 2>/dev/null #fix back cover..
for ((i=0;i < 20;i++)) do

	convert -append "split/majo-$FIRST.png" "split/majo-$LAST.png" "merge/majo-$(printf '%03d' $PAGE).png";
	((PAGE++))
	mogrify -rotate 180 "split/majo-$(($FIRST+3)).png"
	mogrify -rotate 180 "split/majo-$(($LAST-3)).png"
	convert -append "split/majo-$(($FIRST+3)).png" "split/majo-$(($LAST-3)).png" "merge/majo-$(printf '%03d' $PAGE).png"; 
	((PAGE++))

	FIRST=$(($FIRST+2))
	LAST=$(($LAST-2))
done
echo "Done."

#
# BACK
#

echo -n "Joining.. " 
convert -page a4 "merge/majo*.png" fixed.pdf
echo -n "Done."
 
