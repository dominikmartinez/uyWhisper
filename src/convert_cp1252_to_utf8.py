#!usr/bin/env python


import sys


def convert(src, tgt):
    # convert src file and write to tgt file
    with open(src, 'r', encoding='cp1252', errors='replace') as infile:
        text = infile.read()

    with open(tgt, 'w', encoding='utf-8') as outfile:
       outfile.write(text)


def main():
    # check number of args and apply conversion
    args=sys.argv
    assert len(args) > 2
    convert(args[1], args[2])


if __name__ == '__main__':
    main()
