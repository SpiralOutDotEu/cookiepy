import os
from dulwich import porcelain

url = "https://github.com/tensorflow/models.git"
data_folder = "data"
path = os.path.join(data_folder, "models")


def clone_models(models_folder=path, models_url=url):
    os.makedirs(models_folder, exist_ok=True)
    porcelain.clone(models_url, models_folder)
    return True
