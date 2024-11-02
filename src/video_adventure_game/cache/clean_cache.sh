#!/bin/sh

SUFF=wav

for FILE in *.$SUFF
do
    echo "Origin : $FILE"
    rm $FILE
done
echo "DONE !!!"