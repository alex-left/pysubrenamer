#!/usr/bin/python3
''' Simple script to rename subtitles files with the same name of their
respectives video files allocated in the same directory.
This is very convenient because many video players require it.
You can run it over a single file or other files of directory, with path.
Very useful with TV episodes.
'''

import argparse
import pathlib
import re

parser = argparse.ArgumentParser(description="Rename subtitles files with the \
    same filename of their respectives video files \
    allocated in the same directory")
parser.add_argument("target", type=str, nargs='+',
                    help="Subtitle file, video file or directory")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="print every file or directories renamed")
parser.add_argument("-n", "--name", type=str, action="store",
                    help="Filter by name")

args = parser.parse_args()
verbose = args.verbose
name = args.name

video_extensions = [
    "mkv",
    "mp4",
    "mov",
]

sub_extensions = [
    "srt",
    "sub"
]

episodes_patterns = [
    r'[sS][0-9]{1,2}[eE][0-9]{1,2}',
    r'[0-9]{1,2}[xX][0-9]{1,2}'
]

class Subrenamer(type(pathlib.Path())):
    extensions = {
        "video": video_extensions,
        "sub": sub_extensions
    }
    episodes_patterns = episodes_patterns

    def __init__(self, *args, **kwargs):
        self.filter = name
        self.paired = None
        self.episode = None
        self.type = None
        self.detect_type()
        self.detect_episode()
        if self.type == "video":
            self.pair("sub")
        if self.type == "sub":
            self.pair("video")
        if self.paired:
            self.sub_rename()

    def detect_episode(self):
        """Check if file is an episode. The filename must have a string that
        matches a pattern defined in episodes_patterns. Like "GoT_S01E03.mkv"
        """
        for pattern in self.episodes_patterns:
            result = re.search(pattern, self.name)
            if result:
                self.episode = result.group()
                return True
            else:
                return False

    def detect_type(self):
        """check if file have a valid extension of subtitles or videofile"""
        for type in self.extensions.keys():
            for extension in self.extensions[type]:
                if extension.lower() in self.suffix.lower():
                    self.type = type
                    return True

    def pair(self, type):
        """find the respective subtitle or video file. If filename doesn't"""
        if not self.is_file() or not self.type:
            print("{} is not a valid file, no action taken".format(
                  self.absolute()))
            return False
        for pattern in self.extensions[type]:
            if self.filter:
                files = [file for file in self.parent.glob(
                        "*.{}".format(pattern))
                         if self.filter.lower() in file.name.lower()]
            else:
                files = list(self.parent.glob("*.{}".format(pattern)))
            if not self.episode:
                if len(files) > 1:
                    print("more than one file found, no action taken over {}".
                          format(self.absolute()))
                    return False
                if len(files) == 1:
                    self.paired = files[0]
                    return True
            else:
                for file in files:
                    if self.episode in file.name:
                        self.paired = file
                        return True
                return False

    def sub_rename(self):
        if self.stem == self.paired.stem:
            return False
        if self.type == "video":
            self.paired.rename(self.with_suffix(self.paired.suffix))
        if self.type == "sub":
            self.rename(self.with_name(self.paired.stem + self.suffix))


if __name__ == "__main__":
    for arg in args.target:
        Subrenamer(arg)
