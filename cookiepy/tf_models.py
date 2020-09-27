import os
import subprocess
from dulwich import porcelain

url = "https://github.com/tensorflow/models.git"
models = "models"
path = os.path.join(models)


def get_models(models_folder=path, models_url=url):
    os.makedirs(models_folder, exist_ok=True)
    porcelain.clone(models_url, models_folder)
    return True


def install_object_detection(models_path='models'):
    subprocess.run(get_install_script(models_path))
    return True


def get_install_script(models_path='models'):
    cd_to_research = "cd {}/research/; ".format(models_path)
    proto_build = "protoc object_detection/protos/*.proto --python_out=.; "
    copy_setup = "cp object_detection/packages/tf2/setup.py .; "
    pip_install = "python -m pip install .; "
    return cd_to_research + proto_build + copy_setup + pip_install
