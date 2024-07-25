data_dir=/local/scratch/dmartinez/data/claru

align=$data_dir/audio/interviews/alignments
meta_dir=$data_dir/meta
file=50rm.csv  # for development purposes,only one file is processed

# run recutting according to timething readme
timething recut \
    --from-metadata $meta_dir/$file \
    --to-metadata $meta_dir/recut/$file \
    --alignments-dir $align \
    --cut-threshold-seconds 30.0
