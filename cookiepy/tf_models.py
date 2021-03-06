import os
from subprocess import PIPE
import subprocess
from dulwich import porcelain

url = "https://github.com/tensorflow/models.git"
models = "models"
path = os.path.join(models)


def get_models(models_folder=path, models_url=url):
    os.makedirs(models_folder, exist_ok=True)
    porcelain.clone(models_url, models_folder)
    return True


def install_object_detection(models_path=path):
    print(get_install_script(models_path).split())
    res = process = subprocess.run(get_install_script(models_path),
                           shell=True,
                           stdout=PIPE,
                           stderr=PIPE)
    print(res.stdout.decode('utf-8'))
    return True


def get_install_script(models_path='models'):
    cd_to_research = 'cd {}/research/; '.format(models_path)
    ls = 'ls -l; '
    proto_build = 'protoc object_detection/protos/*.proto --python_out=.; '
    copy_setup = 'cp object_detection/packages/tf2/setup.py .; '
    pip_install = 'python -m pip install .; '
    return cd_to_research + ls + proto_build + copy_setup + pip_install
