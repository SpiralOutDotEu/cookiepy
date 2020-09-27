import unittest
from cookiepy import tf_models
from unittest import mock
from dulwich import porcelain

url = "https://github.com/tensorflow/models.git"
default_path = "models"


class TestTfModels(unittest.TestCase):

    @mock.patch('os.makedirs', autospec=True)
    @mock.patch.object(porcelain, 'clone', autospec=True)
    def test_it_clones_models_to_data_models_by_default(self, mock_git_clone, mock_mkdir):
        tf_models.get_models()

        mock_mkdir.assert_called_with(default_path, exist_ok=True)
        mock_git_clone.assert_called_with(url, default_path)

    @mock.patch('os.makedirs', autospec=True, exist_ok=True)
    @mock.patch.object(porcelain, 'clone', autospec=True)
    def test_it_clones_models_to_specified_folder(self, mock_git_clone, mock_mkdir):
        tf_models.get_models(models_folder='zoo/folder')

        mock_mkdir.assert_called_with("zoo/folder", exist_ok=True)
        mock_git_clone.assert_called_with(url, "zoo/folder")
