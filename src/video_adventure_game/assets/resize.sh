#!/bin/sh

SUFF=TS.mp4

for FILE in *.$SUFF
do
    echo "Origin : $FILE"
    NAME=${FILE%.$SUFF}.TSR.mp4
    echo "Rename : $NAME"
    ffmpeg -i $FILE -s 800x450 -filter:v fps=25 $NAME
done
echo "DONE !!!"