#!/bin/bash
#
# 扉

# GRAMMAR

HEAD="https://tobiraweb.9640.jp/wp-content/uploads/L"
TAIL="_grammar_exercise.pdf"

#for i in {01..15}; do
#	wget --no-check-certificate "$HEAD$i$TAIL"
#	sleep 2
#done

# AUDIO

HEAD="https://tobiraweb.9640.jp/wp-content/uploads/L"
TAIL=".zip"

for i in {01..15}; do
        wget --no-check-certificate "$HEAD$i$TAIL"
        sleep 2
done

