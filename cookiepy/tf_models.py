import os
from dulwich import porcelain

url = "https://github.com/tensorflow/models.git"
models = "models"
path = os.path.join(models)


def get_models(models_folder=path, models_url=url):
    os.makedirs(models_folder, exist_ok=True)
    porcelain.clone(models_url, models_folder)
    return True
