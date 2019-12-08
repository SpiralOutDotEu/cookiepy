"""
Usage:
# Create train data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/train
 -o [PATH_TO_ANNOTATIONS_FOLDER]/train_labels.csv

# Create test data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/test
 -o [PATH_TO_ANNOTATIONS_FOLDER]/test_labels.csv
"""

from .files import *
import pandas as pd
import numpy as np
import argparse
import xml.etree.ElementTree as ET


def xml_to_dataframe(path):
    object_list = []
    for xml_file in all_xml_in(path):
        xml_to_object_list(object_list, xml_file)
    objects_dataframe = pd.DataFrame(object_list)
    return objects_dataframe


def dataframe_to_csv(dataframe, file):
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dataframe.to_csv(file, index=None)


def xml_to_object_list(object_list, xml_file):
    tree, root = xml_to_element(xml_file)
    for object_element in all_object_elements_in(root):
        object_list.append(object_element_to_dict(root, object_element))


def xml_to_element(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return tree, root


def all_object_elements_in(root):
    return root.findall("object")


def object_element_to_dict(root_element, object_element):
    value = {
        "filename": root_element.find("filename").text,
        "width": int(root_element.find("size").find("width").text),
        "height": int(root_element.find("size").find("height").text),
        "class": object_element.find("name").text,
        "xmin": int(object_element.find("bndbox").find("xmin").text),
        "ymin": int(object_element.find("bndbox").find("ymin").text),
        "xmax": int(object_element.find("bndbox").find("xmax").text),
        "ymax": int(object_element.find("bndbox").find("ymax").text),
    }
    return value


def classes_from_dataframe(objects_dataframe):
    classes_column = objects_dataframe['class'].to_numpy()
    classes_names = list(set(classes_column))
    classes_names.sort()
    return classes_names


def split_train_test_dataframes(input_dataframe=None,
                                train_ration=0.8):
    msk = np.random.rand(len(input_dataframe)) < train_ration
    output_train_dataframe = input_dataframe[msk]
    output_test_dataframe = input_dataframe[~msk]
    return output_train_dataframe, output_test_dataframe


def write_label_map(objects_dataframe, output_file="data/train data/label_map.pbtxt"):
    classes_names = classes_from_dataframe(objects_dataframe)
    label_map_path = os.path.join(output_file)

    dirname = os.path.dirname(output_file)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    pbtxt_content = ""
    for i, class_name in enumerate(classes_names):
        pbtxt_content = (
            pbtxt_content
            + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(
            i + 1, class_name
        )
        )
    pbtxt_content = pbtxt_content.strip()
    with open(label_map_path, "w") as f:
        f.write(pbtxt_content)

