#!/bin/bash

#
# GET
#

FILE='um-kumonoito.pdf'
PREFIX='ito'

wget -O "$FILE" "https://www.japancenter.cz/upload/files/downloads/$FILE"

#
# EXTRACT
#

echo -n "Extracting.. " 
pdfimages $FILE $PREFIX
echo "Done."

#
# SPLIT
#

INDEX=0

echo -n "Splitting.. " 
mkdir split/ 2>/dev/null
for PAGE in {000..013}; do
	convert -crop 100%x50% "$PREFIX-$PAGE.pbm" "out_%d.pbm"
	mv "out_0.pbm" "split/$PREFIX-$INDEX.pbm"
	((INDEX++))
	mv "out_1.pbm" "split/$PREFIX-$INDEX.pbm"
	((INDEX++))
done
echo "Done."

#
# JOIN
#
#  PAGE ORDER: 1 0 3 2 5 4 7 6 9 .. 25
# PRINT ORDER: 1 27 | 0 26 - 3 25 | 2 24 .. 
#

FIRST=1
LAST=27
PAGE=0

echo -n "Joining.. " 
mkdir merge/ 2>/dev/null

for ((i=0;i < 7 ;i++)) do
	convert -append "split/$PREFIX-$FIRST.pbm" "split/$PREFIX-$LAST.pbm" "merge/$PREFIX-$(printf '%03d' $PAGE).pbm";
	((PAGE++))
	mogrify -rotate 180 "split/$PREFIX-$(($FIRST-1)).pbm"
	mogrify -rotate 180 "split/$PREFIX-$(($LAST-1)).pbm"
	convert -append "split/$PREFIX-$(($FIRST-1)).pbm" "split/$PREFIX-$(($LAST-1)).pbm" "merge/$PREFIX-$(printf '%03d' $PAGE).pbm"; 
	((PAGE++))

	FIRST=$(($FIRST+2))
	LAST=$(($LAST-2))
done
echo "Done."

#
# BACK
#

echo -n "Converting.. " 
convert -compress Group4 -density 400 "merge/$PREFIX*.png" fixed.pdf
echo -n "Done."
 
