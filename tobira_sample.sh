#!/bin/bash

FILE='honsatsu-sample.pdf'

qpdf --decrypt --password='' "$FILE" dec.pdf
pdftk dec.pdf output unc.pdf uncompress
sed -i 's/SAMPLE/      /g' unc.pdf
sed -i 's/onscreen="1"/onscreen="0"/g' unc.pdf
sed -i 's/onprint="1"/onprint="0"/g' unc.pdf
sed -i 's/\/Private \/Watermark/\/Watermark/g' unc.pdf
pdftk unc.pdf output final.pdf compress

