data_dir=/local/scratch/dmartinez/data/claru

audio=$data_dir/audio/interviews/cut/50rm.wav
transcript=$data_dir/transcripts/interviews/preprocessed/50rm.txt

language=spanish # use 'spanish' or 'portuguese'

# run alignment according to timething readme
timething align-long \
    --language $language \
    --audio-file $audio \
    --transcript-file $transcript \
    --alignments-dir $data_dir/audio/interviews/alignments \
    --batch-size 1 \
    --n-workers 5 \
    --use-gpu True 
