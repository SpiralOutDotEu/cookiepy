import unittest
from cookiepy import tf_models
from unittest import mock
from dulwich import porcelain
import subprocess
url = "https://github.com/tensorflow/models.git"
default_path = "models"

cd_to_research = "cd models/research/; "
proto_build = "protoc object_detection/protos/*.proto --python_out=.; "
copy_setup = "cp object_detection/packages/tf2/setup.py .; "
pip_install = "python -m pip install .; "
install_script = cd_to_research + proto_build + copy_setup + pip_install

cd_to_research_custom_models_folder = "cd my_folder/my_model/research/; "
custom_install_script = cd_to_research_custom_models_folder + proto_build + copy_setup + pip_install


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

    def test_it_returns_the_object_detection_install_script(self):
        assert tf_models.get_install_script() == install_script

    def test_it_returns_the_object_detection_install_script_from_another_model_folder(self):
        assert tf_models.get_install_script('my_folder/my_model') == custom_install_script

    @mock.patch.object(subprocess, 'run', autospec=True)
    def test_it_run_object_detection_api_from_default_folder(self, sub_process_run):
        tf_models.install_object_detection()
        sub_process_run.assert_called_with(install_script)

    @mock.patch.object(tf_models, 'get_install_script', autospec=True)
    @mock.patch.object(subprocess, 'run', autospec=True)
    def test_it_run_object_detection_api_from_another_folder(self, sub_process_run, get_install_path):
        some_folder_path = 'folder1/folder2'
        get_install_path.return_value = 'patch'

        tf_models.install_object_detection(models_path=some_folder_path)

        get_install_path.assert_called_with(some_folder_path)
        sub_process_run.assert_called_with('patch')

