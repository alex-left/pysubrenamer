#!/usr/bin/python3
''' Simple script to rename subtitles files with the same name of their
respectives video files allocated in the same directory.
This is very convenient because many video players require it.
You can run it over a single file or other files of directory, with path.
Very useful with TV episodes.
'''

import argparse
from pathlib import Path
import re

VIDEO_EXTENSIONS = {
    "mkv",
    "mp4",
    "mov",
    "avi"
}

SUBTITLE_EXTENSIONS = {
    "srt",
    "sub",
    "ass",
    "ssa"
}

EPISODES_RE_PATTERNS = [
    r'[sS]([0-9]{1,2})[\.\-_]?[eE]([0-9]{1,2})',
    r'([0-9]{1,2})[xX]([0-9]{1,2})'
]


class File:
    def __init__(self, filename):
        self.path = Path(filename)
        # suffix returns the dot, we remove it
        self.extension = self.path.suffix[1:]
        self.season = None
        self.episode = None
        self.detect_episode()

    def is_subtitle(self):
        return self.extension in SUBTITLE_EXTENSIONS

    def is_video(self):
        return self.extension in VIDEO_EXTENSIONS

    def is_episode(self):
        return bool(self.season and self.episode)

    def is_valid(self):
        return bool(self.is_video() or self.is_subtitle())

    def detect_episode(self):
        for pattern in EPISODES_RE_PATTERNS:
            result = re.search(pattern, self.path.stem)
            if result:
                self.season = int(result.groups()[0])
                self.episode = int(result.groups()[1])

    def rename(self, target):
        if not self.is_subtitle():
            raise TypeError("Only can rename subtitles",
                            "Filename: {} is not valid".format(self.path))
        return self.path.rename(target.path.with_suffix(self.path.suffix))


def search_pair(file):
    '''return the associated opposite file(video or subtitle) for a given file
    or returns FileNotFoundError exception'''
    current_dir = file.path.resolve().parent
    current_files = [File(file) for file in current_dir.iterdir() if file.is_file()]
    valid_files = []

    # ensure only use the opposite type
    if file.is_video():
        valid_files = [file for file in current_files if file.is_subtitle()]
    elif file.is_subtitle():
        valid_files = [file for file in current_files if file.is_video()]

    if len(valid_files) == 1:
        return valid_files[0]
    for item in valid_files:
        if (item.season == file.season and item.episode == file.episode):
            return item
    raise FileNotFoundError("Not paired file found for {}".format(file.path))


def renamer(file, name):
    print(file, name)
    print(type(file), type(name))
    file.rename(name)


def process_file(file):
    target = File(file)
    if not target.is_valid():
        print("{} is not a valid file".format(file))
        return
    try:
        pair = search_pair(target)
        if pair.is_subtitle():
            renamer(pair, target)
        if pair.is_video():
            renamer(target, pair)
    except FileNotFoundError as e:
        print(e)
        return


def main(args):
    for arg in args:
        target = Path(arg)
        if target.is_dir():
            for file in target.iterdir():
                process_file(file)
        if target.is_file():
            process_file(target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename subtitles files with the \
        same filename of their respectives video files \
        allocated in the same directory")
    parser.add_argument("target", type=str, nargs='+',
                        help="Subtitle file, video file or directory")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print every file or directories renamed", default=False)
    parser.add_argument("-n", "--name", type=str, action="store",
                        help="Filter by name", default=None)
    args = parser.parse_args()
    verbose = args.verbose
    name = args.name
    main(args.target)

    # class Subrenamer(type(pathlib.Path())):
    #     extensions = {
    #         "video": video_extensions,
    #         "sub": sub_extensions
    #     }
    #     episodes_patterns = episodes_patterns
    #     verbose = verbose

    #     def __init__(self, path=None, *args, **kwargs):
    #         """Initialize the object"""
    #         super().__init__()
    #         self.filter = name
    #         self.paired = None
    #         self.tv = {}
    #         self.type = None
    #         self.detect_type()

    #     def run(self):
    #         """Main workflow. Check if user's argument are a dir or file. Check
    #         the video extension. If file have an unvalid extension or not exist,
    #         don't do anything."""
    #         if self.type == "dir":
    #             self.dir_mode()
    #             return True
    #         if self.type == "video":
    #             self.pair("sub")
    #         if self.type == "sub":
    #             self.pair("video")
    #         if self.paired:
    #             self.sub_rename()

    #     def dir_mode(self):
    #         """Instantiate a subrenamer object for each file in given dir"""
    #         for file in self.iterdir():
    #             if file.is_file():
    #                 file.__init__()
    #                 file.run()

    #     def detect_episode(self):
    #         """Check if file is an episode. The filename must have a string that
    #         matches a pattern defined in episodes_patterns. Like "GoT_S01E03.mkv"
    #         """
    #         for pattern in self.episodes_patterns:
    #             result = re.search(pattern, self.name)
    #             if result:
    #                 self.tv["season"] = int(result.groups()[0])
    #                 self.tv["episode"] = int(result.groups()[1])
    #                 return True
    #         return False

    #     def detect_type(self):
    #         """check if file have a valid extension of subtitles or videofile
    #         or is if a directory"""
    #         if self.is_dir():
    #             self.type = "dir"
    #             return True
    #         if not self.is_file():
    #             print("{} is not a valid filename or not exists, no action taken".format(
    #                   self.absolute()))
    #             return False
    #         self.detect_episode()
    #         for type in self.extensions.keys():
    #             for extension in self.extensions[type]:
    #                 if extension.lower() in self.suffix.lower():
    #                     self.type = type
    #                     return True

    #     def pair(self, type):
    #         """Find the respective subtitle or video file."""
    #         for pattern in self.extensions[type]:
    #             if self.filter:
    #                 files = [file for file in self.parent.glob(
    #                     "*.{}".format(pattern))
    #                     if self.filter.lower() in file.name.lower()]
    #             else:
    #                 files = list(self.parent.glob("*.{}".format(pattern)))
    #             if not self.tv:
    #                 if len(files) > 1:
    #                     print("more than one file found, no action taken over {}".
    #                           format(self.absolute()))
    #                     return False
    #                 if len(files) == 1:
    #                     self.paired = files[0]
    #                     return True
    #             else:
    #                 for file in files:
    #                     file.__init__()
    #                     if (self.tv["episode"] == file.tv["episode"] and
    #                             self.tv["season"] == file.tv["season"]):
    #                         self.paired = file
    #                         return True
    #                 return False

    #     def print_renamed(self, file):
    #         """Small function to respect KISS principle in sub_rename method."""
    #         if self.verbose:
    #             print("{} renamed".format(file))

    #     def sub_rename(self):
    #         """Rename the subtitle with his respective videofile paired if is
    #         necessary."""
    #         if self.stem == self.paired.stem:
    #             if self.verbose:
    #                 print("found files with same name, no action taken over {}".
    #                       format(self.absolute()))
    #             return False
    #         if self.type == "video":
    #             self.print_renamed(self.paired.absolute())
    #             self.paired.rename(self.with_suffix(self.paired.suffix))
    #         if self.type == "sub":
    #             self.print_renamed(self.absolute())
    #             self.rename(self.with_name(self.paired.stem + self.suffix))

    # if __name__ == "__main__":
    #     for arg in args.target:
    #         target = Subrenamer(arg)
    #         target.run()
