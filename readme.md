# Pysubrenamer

Rename subtitle file with the same name of their respective video files. Ideal for TV chapters

## Description
Pysubrenamer rename the subtitle file if the filename have the same episode pattern and if
both are in same directory. Also you can rename the subtitle file if
in the directory only exists one video file and one subtitle file without check the filename
Also you can use an aditionally text filter.

This script is very useful with TV episodes, when you have downloaded all chapters and by
other way you have downloaded the subtitles but they have a diferent name and you need to have
the same name in order to the video player can take the correct subtitles automatically.

If in the directory you have more than one video file and subtitle file,
pysubrenamer don't do anything.

Only works with following file extensions:

```
video_extensions = [
    "mkv",
    "mp4",
    "mov",
]

sub_extensions = [
    "srt",
    "sub"
]
```

If you want more extensions you can edit the script or do a pull request.

The script will detect the episodes with pattern "S01E01" or "1x1", you can add
more regex patterns if is needed into script. Note that you must
create a group (enclosing in parenthesis) for each number of season and episode.

```
episodes_patterns = [
    r'[sS]([0-9]{1,2})[eE]([0-9]{1,2})',
    r'([0-9]{1,2})[xX]([0-9]{1,2})'
]
```

## Getting Started

### Prerequisites

- Only needs python3. Only tested in linux, but should work in Mac or Windows.

### Installing

- Clone this project:
```
git clone https://github.com/alex-left/pysubrenamer
```
- run setup:
```
sudo python3 setup.py install
```

## USAGE

```
usage: pysubrenamer.py [-h] [-v] [-n NAME] target [target ...]

Rename subtitles files with the same filename of their respectives video files
allocated in the same directory

positional arguments:
  target                Subtitle file, video file or directory

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print every file or directories renamed
  -n NAME, --name NAME  Filter by name

```
