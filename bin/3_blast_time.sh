#!/bin/bash

dir=blast.out
if (($# == 1)); then
    dir=$1
fi             

if [ -d $dir ]; then
    cd $dir
fi
grep time *end | perl -pe 's/.end\S+ /\t/; s/ hours//'
