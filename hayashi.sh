#!/bin/bash

#
# GET
#

FILE='um-hayashi-no-okude.pdf'
PREFIX='hayashi'

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
for PAGE in {000..041}; do
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
#  PAGE ORDER: 0 2 3 4 5 6 7 8 9 .. 1
# PRINT ORDER: 0 83 | 1 82 - 2 81 | 3 80 - 4 79  .. 
#

FIRST=0
LAST=83
PAGE=0

echo -n "Joining.. " 
mkdir merge/ 2>/dev/null

for ((i=0;i < 21 ;i++)) do
	mogrify -rotate 180 "split/$PREFIX-$FIRST.pbm"
	mogrify -rotate 180 "split/$PREFIX-$LAST.pbm"
	convert -append "split/$PREFIX-$FIRST.pbm" "split/$PREFIX-$LAST.pbm" "merge/$PREFIX-$(printf '%03d' $PAGE).pbm";
	((PAGE++))
	convert -append "split/$PREFIX-$(($FIRST+1)).pbm" "split/$PREFIX-$(($LAST-1)).pbm" "merge/$PREFIX-$(printf '%03d' $PAGE).pbm"; 
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
 
