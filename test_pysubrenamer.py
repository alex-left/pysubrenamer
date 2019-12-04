from collections import namedtuple
import unittest
from unittest.mock import patch
from parameterized import parameterized
import pysubrenamer
import pathlib
import shutil


integration_files = [
    ["example.mkv",
     "example.s01e02.mkv",
     "example.s01e03.mkv",
     "example.s02e04.mkv",
     "example.s03e01.mkv",
     "subtitle.s01e02.srt",
     "subtitle.s01e03.srt",
     "subtitle.s02e04.srt",
     "subtitle.s03e01.srt",
     "fakefile.txt",
     "example.srt"
     ],
    ['example.mkv',
     'example.s01e02.mkv',
     'example.s01e02.srt',
     'example.s01e03.mkv',
     'example.s01e03.srt',
     'example.s02e04.mkv',
     'example.s02e04.srt',
     'example.s03e01.mkv',
     'example.s03e01.srt',
     'example.srt',
     'fakefile.txt'
     ]
]

detect_episode_cases = [
    ("some.video.s01e08.mkv", True),
    ("some.video.2x05.mkv", True),
    ("some.video.mkv", False),
    ("some.subtitle.s03e05.srt", True),
    ("some.video.S1E20.mkv", True),
    ("some.subtitle.srt", False)
]

rename_fail_cases = [
    ("example.jpg", TypeError),
    ("example.mkv", TypeError)
]

Cases_mocked_tuple = namedtuple("Cases_mocked_tuple", ["case", "mock", "expected"])
search_pair_cases = [
    Cases_mocked_tuple(case="example.mp4",
                       mock=("a", "b", "example.mkv", "example.srt"),
                       expected="example.srt"),
    Cases_mocked_tuple(case="example.s03e07.mkv",
                       mock=("bad.s03e08.srt", "example.s03e07.srt", "example.srt"),
                       expected="example.s03e07.srt"),
    Cases_mocked_tuple(case="example.mkv",
                       mock=("bad.s03e08.srt", "example.s03e07.srt", "example.srt"),
                       expected="example.srt")
]

search_pair_fail_cases = [
    Cases_mocked_tuple(case="example.jpg",
                       mock=("bad.s03e08.srt", "example.s03e07.srt", "example.srt"),
                       expected=FileNotFoundError),
    Cases_mocked_tuple(case="example.mkv",
                       mock=("bad.s03e08.jpg",),
                       expected=FileNotFoundError)
]


class TestRenamer(unittest.TestCase):

    @parameterized.expand(detect_episode_cases)
    def test_detect_episode(self, case, expected):
        file = pysubrenamer.File(case)
        self.assertEqual(file.is_episode(), expected)

    @parameterized.expand(rename_fail_cases)
    def test_only_rename_subtitles(self, case, expected):
        file = pysubrenamer.File(case)
        with self.assertRaises(expected):
            file.rename("some.example")

    @parameterized.expand(search_pair_cases)
    @patch('pathlib.Path.is_file', autospec=True)
    @patch('pathlib.Path.iterdir', autospec=True)
    def test_search_pair(self, case, mock, expected, mocked_iterdir, mocked_is_file):
        mocked_is_file.return_value = True
        mocked_iterdir.return_value = (pathlib.Path(file) for file in mock)
        file = pysubrenamer.File(case)
        self.assertEqual(pysubrenamer.search_pair(file).path, pysubrenamer.File(expected).path)

    @parameterized.expand(search_pair_fail_cases)
    @patch('pathlib.Path.is_file', autospec=True)
    @patch('pathlib.Path.iterdir', autospec=True)
    def test_search_pair_exceptions(self, case, mock, expected, mocked_iterdir, mocked_is_file):
        mocked_is_file.return_value = True
        mocked_iterdir.return_value = (pathlib.Path(file) for file in mock)
        file = pysubrenamer.File(case)
        with self.assertRaises(expected):
            pysubrenamer.search_pair(file)


class TestMainProgram(unittest.TestCase):
    tmpdir = pathlib.Path("/tmp/pysubrenamer-tests")

    def prepare(self, dataset):
        if self.tmpdir.exists():
            shutil.rmtree(self.tmpdir)
        self.tmpdir.mkdir()
        for file in dataset:
            f = pathlib.Path(self.tmpdir/file)
            f.write_bytes(bytes(2))

    def test_dir_with_multiple_files(self):
        self.prepare(integration_files[0])
        pysubrenamer.main(list(self.tmpdir.iterdir()))
        self.assertEqual(sorted(n.name for n in self.tmpdir.iterdir()), integration_files[1])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)


if __name__ == '__main__':
    unittest.main()
