#!/usr/bin/env python


import sys
import os
import re
import subprocess
import shutil


class AudioCutter(object):
    def __init__(self, audio_dir, transcript_dir):
        self.__audio_dir = audio_dir
        self.__transcript_dir = transcript_dir

        self.time_pattern = re.compile(r"(\d{1,2}:\d{2}:\d{2})")
        self.ffmpeg = './ffmpeg-git-20240524-amd64-static/ffmpeg'


    def determine_need_for_cut(self, transcript, window):
        # determine whether the transcription time stamps match the total time
        if "0:00:00" not in window[0]:
            return True

        with open(transcript, "r") as infile:
            lines = infile.readlines()
            total_time = self.time_pattern.search(lines[1]).group(1)
        if total_time != window[1]: ## this is true when one stamp contains '0:' and the other '00:' but does not affect behaviour negatively
            return True

        return False


    def get_time_window(self, transcript):
        # extract transcription time stamps from second line of metadata
        with open(transcript, "r") as infile:
            lines = infile.readlines()

        matches = self.time_pattern.findall(lines[2])
        return matches


    def process_pair(self, pair):
        # for a pair of audio and transcription, determine need for cut and then cut the audio
        audio = os.path.join(self.__audio_dir, pair[0])
        new_audio = os.path.join(self.__audio_dir, "cut", pair[0])
        transcript = os.path.join(self.__transcript_dir, pair[1])

        window = self.get_time_window(transcript)

        need_for_cut = self.determine_need_for_cut(transcript, window)

        if need_for_cut:
            subprocess.run([self.ffmpeg, "-i", audio, "-ss", window[0], "-to", window[1], "-c", "copy", new_audio])
        else:  # if no need for cut, copy audio to output directory
            shutil.copy(audio, new_audio)


    def process_files(self):
        # process all files in given directory
        audio_filenames = [f for f in os.listdir(self.__audio_dir) if os.path.isfile(os.path.join(self.__audio_dir, f))]
        transcript_filenames = [f for f in os.listdir(self.__transcript_dir) if os.path.isfile(os.path.join(self.__transcript_dir, f))]
        paired_filenames = zip(audio_filenames, transcript_filenames)

        for pair in paired_filenames:
            print(pair)
            self.process_pair(pair)


def main():
    assert len(sys.argv) > 2, "directory path is required as positional argument"
    audio_dir = sys.argv[1]
    transcript_dir = sys.argv[2]
    ac = AudioCutter(audio_dir, transcript_dir)
    ac.process_files()


if __name__ == '__main__':
    ## usage: python cut_audios.py path/to/audio_dir path/to_transcript_dir
    main()
