from unittest.mock import MagicMock, patch
import unittest
from unittest import mock
import os
import cookiepy as cp


def mock_fs(folder):
    return [
            ('/foo', ('bar',), ('baz',)),
            ('/foo/bar', (), ('not_image.xyz', 'image1.jpg')),
            ('/foo/baz', (), ('not_image.xyz', 'image2.jpeg')),
            ]


class TestFiles(unittest.TestCase):

    @mock.patch('os.walk', side_effect=mock_fs)
    def test_it_gets_all_images_in_folder(self, mock_fs):
        expected = ['/foo/bar/image1.jpg', '/foo/baz/image2.jpeg']
        result = cp.get_all_images_in("/test/folder")
        assert list(result) == expected

    def test_it_checks_if_is_image(self):
        assert (cp.is_image("file.jpg") is True)
        assert (cp.is_image("file.jpeg") is True)
        assert (cp.is_image("file.png") is False)
        assert (cp.is_image("file.jp2") is False)
        assert (cp.is_image("file.jpag") is False)
