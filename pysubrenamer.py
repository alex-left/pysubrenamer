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
    verbose = verbose

    def __init__(self, *args, **kwargs):
        """Initialize the object and init the renamer process."""
        self.filter = name
        self.paired = None
        self.episode = None
        self.type = None
        self.run()

    def run(self):
        """Main workflow. Check if user's argument are a dir or file. Check
        the video extension. If file have an unvalid extension or not exist,
        don't do anything."""
        self.detect_type()
        if self.type == "dir":
            self.dir_mode()
            return True
        if self.type == "video":
            self.pair("sub")
        if self.type == "sub":
            self.pair("video")
        if self.paired:
            self.sub_rename()

    def dir_mode(self):
        """Instantiate a subrenamer object for each file in given dir"""
        for file in self.iterdir():
            if file.is_file():
                Subrenamer(file.__str__())

    def detect_episode(self):
        """Check if file is an episode. The filename must have a string that
        matches a pattern defined in episodes_patterns. Like "GoT_S01E03.mkv"
        """
        for pattern in self.episodes_patterns:
            result = re.search(pattern, self.name)
            if result:
                self.episode = result.group()
                return True
        return False

    def detect_type(self):
        """check if file have a valid extension of subtitles or videofile
        or is if a directory"""
        if self.is_dir():
            self.type = "dir"
            return True
        if not self.is_file():
            print("{} is not a valid file, no action taken".format(
                  self.absolute()))
            return False
        self.detect_episode()
        for type in self.extensions.keys():
            for extension in self.extensions[type]:
                if extension.lower() in self.suffix.lower():
                    self.type = type
                    return True

    def pair(self, type):
        """Find the respective subtitle or video file."""
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

    def print_renamed(self):
        """Small function to respect KISS principle in sub_rename method."""
        if self.verbose:
            print("{} renamed".
                  format(self.absolute()))

    def sub_rename(self):
        """Rename the subtitle with his respective videofile paired if is
        necessary."""
        if self.stem == self.paired.stem:
            if self.verbose:
                print("found files with same name, no action taken over {}".
                      format(self.absolute()))
            return False
        if self.type == "video":
            self.print_renamed()
            self.paired.rename(self.with_suffix(self.paired.suffix))
        if self.type == "sub":
            self.print_renamed()
            self.rename(self.with_name(self.paired.stem + self.suffix))


if __name__ == "__main__":
    for arg in args.target:
        Subrenamer(arg)
