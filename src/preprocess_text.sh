#!/bin/bash

data_dir=/local/scratch/dmartinez/data/claru/transcripts/interviews
mkdir -p $data_dir/preprocessed

for file in $data_dir/*.txt
do
    base_name=$(basename $file .txt)
    utf=$(mktemp)
    tmp=$(mktemp)
    tmp2=$(mktemp)
    output="$data_dir/preprocessed/$base_name.txt"

    # convert encoding of text files (note that first variant leads to problems with newlines)
    # iconv -f cp1252 -t utf-8//IGNORE $file > $utf
    python src/convert_cp1252_to_utf8.py $file $utf

    # delete first 4 lines, select second column, remove newlines, run cleaning script, write to output
    sed '1,4d' $utf | cut -f2 | tr '\n' ' ' | python src/clean_meta.py > $output

    # create input for timething recutting
    meta="$data_dir/../../meta/$base_name.csv"
    echo -n "../audio/interviews/cut/$base_name.wav|" > $meta
    cat $output >> $meta

    rm $utf $tmp $tmp2
done
