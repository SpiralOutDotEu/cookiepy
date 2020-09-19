import unittest
from cookiepy.tf_models import clone_models
from unittest import mock
from unittest.mock import MagicMock, patch
from pygit2 import clone_repository
import os


# def mock_git_clone():
#     return True
#
#
# def mock_mkdir():
#     return True
url = "https://github.com/tensorflow/models.git"
data_folder = "data"
path = os.path.join(data_folder, "models")


class TestModelZoo(unittest.TestCase):

    @mock.patch('os.mkdir')
    @mock.patch('pygit2.clone_repository')
    def test_it_clones_models_to_data_models_by_default(self, mock_git_clone, mock_mkdir):
        mock_git_clone().return_value(True)
        mock_mkdir().return_value(True)

        clone_models()

        mock_mkdir.assert_called_with("data/models")
        mock_git_clone.called_with(url, path,
                                   bare=False,
                                   repository=None,
                                   remote=None,
                                   checkout_branch=None,
                                   callbacks=None)
        assert mock_mkdir.called

    @mock.patch('os.mkdir')
    @mock.patch('pygit2.clone_repository')
    def test_it_clones_models_to_specified_folder(self, mock_git_clone, mock_mkdir):
        mock_git_clone().return_value(True)
        mock_mkdir().return_value(True)
        clone_models(models_folder='zoo/folder')
        mock_mkdir.assert_called_with("zoo/folder")
        mock_git_clone.called_with(url, "zoo/folder",
                                   bare=False,
                                   repository=None,
                                   remote=None,
                                   checkout_branch=None,
                                   callbacks=None)
