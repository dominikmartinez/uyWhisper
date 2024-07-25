#!/usr/bin/env python


import sys
import os
import re
import csv

import argparse

from datasets import Dataset, DatasetDict, Audio
from transformers import WhisperFeatureExtractor, WhisperTokenizer


def whisper_stuff():
    # initialise Whisper-specific things
    feature_extractor = WhisperFeatureExtractor.from_pretrained("openai/whisper-small")
    tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-small")


def create_dataset(splits):
    # create dataset structure
    dataset = DatasetDict()
    for split, data in splits.items():
        dataset[split] = load_data(data)

    print(dataset)

    return dataset


def load_data(split):
    # load data splits both for audio and text 
    audios = [os.path.join(split, file) for file in os.listdir(split) if os.path.isfile(os.path.join(split, file)) and file.endswith(".wav")]
    print(audios)
    audio_dataset = Dataset.from_dict({"audio": audios}).cast_column("audio", Audio())
    print(type(audio_dataset))
    print(audio_dataset[0]["audio"])
    return audio_dataset

    texts = [os.path.join(split, file) for file in os.listdir(split) if os.path.isfile(os.path.join(split, file)) and file.endswith(".txt")]


def parse_arguments():
    parser = argparse.ArgumentParser()

    # get train/dev/test for src audio
    parser.add_argument("--train", type=str, help="directory of train set")
    parser.add_argument("--dev", type=str, help="directory of dev set")
    parser.add_argument("--test", type=str, help="directory of test set")

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

    dataset = create_dataset({
        "train": args.train,
        "dev": args.dev,
    })


if __name__ == '__main__':
    ## usage: python quantify_variants.py /path/to/files
    main()
