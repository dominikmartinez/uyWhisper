#!/usr/bin/env python


import sys
import re


def process_text(text):
    # remove meta comments (round parentheses and squared brackets, and their content)
    text1 = re.sub(r'\(.*?\)|\[.*?\]', '', text)
    # remove language labels (braces, angle brackets, and slashes)
    text2 =re.sub(r'[\{\}<>/]', '', text1)
    return text2


def main():
    # apply processing function to stdin and write to stdout
    input_text = sys.stdin.read()
    processed_text = process_text(input_text)
    sys.stdout.write(processed_text)


if __name__ == '__main__':
    main()
