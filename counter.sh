#!/bin/bash

FIRST=`ls $1/*.tiff | cut -d'_' -f2 | sort | head -1`
LAST=`ls $1/*.tiff | cut -d'_' -f2 | sort | tail -1`
./counter.py $1 $FIRST $LAST | tee $1/results.csv
