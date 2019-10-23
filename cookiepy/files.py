import os


def all_images_in(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if (is_image(file)):
                yield os.path.join(dirpath, file)


def all_xml_in(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if (is_xml(file)):
                yield os.path.join(dirpath, file)


def is_image(file):
    image_suffixes = (".jpg", ".jpeg")
    return True if file.endswith(image_suffixes) else False


def is_xml(file):
    return True if file.endswith(".xml") else False
