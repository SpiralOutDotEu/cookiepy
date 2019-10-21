import os


def get_images(folder):
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for file in filenames:
            if (is_image(file)):
                yield os.path.join(dirpath, file)


def is_image(file):
    image_suffixes = (".jpg", ".jpeg")
    return True if file.endswith(image_suffixes) else False
