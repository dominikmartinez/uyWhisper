#!/usr/bin/env python

import sys
import os
import re
import csv

from nltk.tokenize import word_tokenize

from rich.console import Console
from rich.table import Table


def strip_punctuation(token):
    # strip punctuation from words, e.g. "parto…" -> "parto"
    return re.sub("[^\w\s]", "", token)


def additional_tokenization(text):
    # some additional tokenization that won't be catched by NLTK's tokenizer
    text = re.sub("¿", "¿ ", text)
    return text


def separate_labels(text):
    # separate labels from tokens that haven't been catched by NLTK's tokenizer (affects only the hybrid label)
    new_text = list()

    for i, word in enumerate(text):
        if word[0] == "/" and word[-1] == "/":
            new_text.append("/")
            new_text.append(word[1:-1])
            new_text.append("/")
        elif word[0] == "/":
            new_text.append("/")
            new_text.append(word[1:])
        elif word[-1] == "/":
            new_text.append(word[:-1])
            new_text.append("/")
        else:
            new_text.append(word)

    return new_text

def count_tokens(text):
    # core function that counts the tokens of a string w.r.t. to their label
    # it uses a stack algorithm to count open, nested labels

    # preprocessing
    text = additional_tokenization(text)
    text = word_tokenize(text)
    text = separate_labels(text)

    # initialise variables
    open_labels = ["<", "{"]
    close_labels = [">", "}"]
    open_skip = ["(", "["]
    close_skip = [")", "]"]
    stack = ["unk"]
    current_label = "unk"
    skip = False
    counts = {"{": 0, "<": 0, "/": 0, "unk": 0}

    # counting algorithm
    # skips content between parenthesis or square brackets (this feature is not required anymore with correct preprocessing)
    # determines the category of each token using a label stack
    for token in text:
        if skip == True:
            if token in close_skip:
                skip = False
            continue

        if token in open_skip:
            skip = True
            continue
        elif token in open_labels:
            stack.append(token)
            current_label = token
        elif token in close_labels:
            stack.pop(-1)
            current_label = stack[-1]
            # this block serves for debugging purposes and might still be needed in the future
            #try:
                #current_label = stack[-1]
            #except IndexError:
                #print("-" * 5)
                #print(f"incomplete labels: {text}")
                #pass
        elif token == "/":
        # special treatment for "/" labels because opening and closing labels use the same character
            if current_label == "/":
                stack.pop(-1)
                current_label = stack[-1]
            else:
                stack.append(token)
                current_label = token
        else:
            token = strip_punctuation(token)

            if token.isalpha() is False:
                continue
            counts[current_label] += 1

    freqs = {"es": counts["<"], "pt": counts["{"], "hyb": counts["/"], "unk": counts["unk"]}
    return freqs


def process_line(line):
    # get speaker ID, process text data
    try:
        speaker, text = line.split("\t")
    # this try except block serves for debugging purposes and finds invalid data snippets
    except ValueError:
        print(line)
        print("\t" in line)
        return

    freqs = count_tokens(text)

    # for clarity, the interviewer is excluded from the results
    # unlabelled data is reported to improve the data
    if speaker != "bgarrido":
        if freqs["unk"] > 0:
            print("----\n" + f"fragment with unknown categories: {line}")

    return speaker, freqs


def quantify_variants(lines):
    # process a list of strings and call the main functions on a per-line basis
    freqs = dict()
    for line in lines:
        line = line.strip()
        if "\t" not in line:
            continue
        processed_line = process_line(line)
        if processed_line is None:
            continue
        speaker, freqs_in_line = processed_line

        if speaker not in freqs:
            freqs[speaker] = {"es": 0, "pt": 0, "hyb": 0, "unk": 0}

        for key in freqs_in_line:
                freqs[speaker][key] += freqs_in_line[key]

    return freqs


def print_to_terminal(frequencies, columns):
    #print results to command line by using the "console" utility
    table = Table(title="frequencies")
    rows = [[str(v) for v in d.values()] for d in frequencies]
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*row, style='bright_green')
    console = Console()
    console.print(table)


def process_files(directory):
    # process the files of a directory and compute absolute/relative counts
    all_frequencies = list()
    field_names = ["speaker", "file", "es", "es %", "pt", "pt %", "hyb", "hyb %"]
    filenames = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for filename in filenames:
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as infile:
            lines = infile.readlines()

        print("\n" + f"processing file {filename}")
        results = quantify_variants(lines)

        for k, v in results.items():
            es = v["es"]
            pt = v["pt"]
            hyb = v["hyb"]
            total = es + pt + hyb
            if total == 0:
                continue
            es_relative = round(100 * es / total, 1)
            pt_relative = round(100 * pt / total, 1)
            hyb_relative = round(100 * hyb / total, 1)

            all_frequencies.append({"speaker": k, "file": filename, "es": es, "es %": es_relative, "pt": pt, "pt %": pt_relative, "hyb": hyb, "hyb %": hyb_relative})

    print_to_terminal(all_frequencies, field_names)

    # write results to file
    with open ("results.tsv", "w") as outfile:
        print("writing results...")
        writer = csv.DictWriter(outfile, fieldnames=field_names, delimiter="\t")
        writer.writeheader()
        writer.writerows(all_frequencies)


def main():
    assert len(sys.argv) > 1, "directory path is required as positional argument"
    directory = sys.argv[1]
    process_files(directory)


if __name__ == '__main__':
    ## usage: python quantify_variants.py /path/to/files
    main()
