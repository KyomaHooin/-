#!/bin/bash

#
# GET
#

FILE='um-yokohama-mystery.pdf'
PREFIX='yokohama'

#wget -O "$FILE" "https://www.japancenter.cz/upload/files/downloads/$FILE"

#
# EXTRACT
#

#echo -n "Extracting.. " 
#pdfimages -png $FILE $PREFIX
#echo "Done."

#
# SPLIT
#

#INDEX=0

#echo -n "Spliting.. " 
#mkdir split/ 2>/dev/null
#for PAGE in {000..026}; do
#	convert -crop 100%x50% "$PREFIX-$PAGE.png" "out_%d.png"
#	mv "out_0.png" "split/$PREFIX-$INDEX.png"
#	((INDEX++))
#	mv "out_1.png" "split/$PREFIX-$INDEX.png"
#	((INDEX++))
#done
#echo "Done."

#exit 1

#
# JOIN
#
#  PAGE ORDER: 0 2 3 4 5 6 7 8 9 .. 1
# PRINT ORDER: 1 54 | 2 53 - 2 79 | 5 76 - 4 77 | 7 74 - .. 
#

FIRST=1
LAST=54
PAGE=0

echo -n "Joining.. " 
mkdir merge/ 2>/dev/null
mv "split/$PREFIX-1.png" "split/$PREFIX-$LAST.png" 2>/dev/null #fix back cover..
mv "split/$PREFIX-0.png" "split/$PREFIX-$FIRST.png" 2>/dev/null #fix back cover..
for ((i=0;i < 20 ;i++)) do
	mogrify -rotate 180 "split/$PREFIX-$FIRST.png"
	mogrify -rotate 180 "split/$PREFIX-$LAST.png"
	convert -append "split/$PREFIX-$FIRST.png" "split/$PREFIX-$LAST.png" "merge/$PREFIX-$(printf '%03d' $PAGE).png";
	((PAGE++))
	convert -append "split/$PREFIX-$(($FIRST+1)).png" "split/$PREFIX-$(($LAST-1)).png" "merge/$PREFIX-$(printf '%03d' $PAGE).png"; 
	((PAGE++))

	FIRST=$(($FIRST+2))
	LAST=$(($LAST-2))
done
echo "Done."

exit 1

#
# BACK
#

echo -n "Joining.. " 
convert -limit thread 2 -page a4 "merge/$PREFIX*.png" fixed.pdf
echo -n "Done."
 
