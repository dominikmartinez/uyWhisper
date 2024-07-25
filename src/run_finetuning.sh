source ../venvs/venv_uyWhisper/bin/activate

data_dir=/local/scratch/dmartinez/data/claru

# run our own finetuning script
python src/finetune.py \
    --train $data_dir/train \
    --dev $data_dir/dev
