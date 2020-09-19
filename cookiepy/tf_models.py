import os
import pygit2

url = "https://github.com/tensorflow/models.git"
data_folder = "data"
path = os.path.join(data_folder, "models")


def clone_models(models_folder=path, models_url=url):
    os.mkdir(models_folder)
    pygit2.clone_repository(url, path,
                            bare=False,
                            repository=None,
                            remote=None,
                            checkout_branch=None,
                            callbacks=None
                            )

    return True
