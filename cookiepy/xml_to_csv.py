"""
Usage:
# Create train data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/train
 -o [PATH_TO_ANNOTATIONS_FOLDER]/train_labels.csv

# Create test data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/test
 -o [PATH_TO_ANNOTATIONS_FOLDER]/test_labels.csv
"""

import os
from .files import *
import pandas as pd
import argparse
import xml.etree.ElementTree as ET


def xml_to_element(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return tree, root


def xml_to_dataframe(path):
    object_list = []
    for xml_file in all_xml_in(path):
        tree, root = xml_to_element(xml_file)
        for object in all_object_elements_in(root):
            append_object_element_to_list(root, object, object_list)
    objects_dataframe = pd.DataFrame(object_list)
    classes_names = classes_from_dataframe(objects_dataframe)
    return objects_dataframe, classes_names


def append_object_element_to_list(root, object_element, object_list):
    value = object_to_dict(root, object_element)
    object_list.append(value)


def classes_from_dataframe(objects_dataframe):
    classes_column = objects_dataframe['class'].to_numpy()
    classes_names = list(set(classes_column))
    classes_names.sort()
    return classes_names


def object_to_dict(root_element, object_element):
    value = {
        "filename": root_element.find("filename").text,
        "width": int(root_element.find("size")[0].text),
        "height": int(root_element.find("size")[1].text),
        "class": object_element[0].text,
        "xmin": int(object_element[4][0].text),
        "ymin": int(object_element[4][1].text),
        "xmax": int(object_element[4][2].text),
        "ymax": int(object_element[4][3].text),
    }
    return value


def all_object_elements_in(root):
    return root.findall("object")


def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Sample TensorFlow XML-to-CSV converter"
    )
    parser.add_argument(
        "-i",
        "--inputDir",
        help="Path to the folder where the input .xml files are stored",
        type=str,
    )
    parser.add_argument(
        "-o", "--outputFile",
        help="Name of output .csv file (including path)",
        type=str
    )

    parser.add_argument(
        "-l",
        "--labelMapDir",
        help="Directory path to save label_map.pbtxt file is specified.",
        type=str,
        default="",
    )

    args = parser.parse_args()

    if args.inputDir is None:
        args.inputDir = os.getcwd()
    if args.outputFile is None:
        args.outputFile = args.inputDir + "/labels.csv"

    assert os.path.isdir(args.inputDir)
    os.makedirs(os.path.dirname(args.outputFile), exist_ok=True)
    xml_df, classes_names = xml_to_dataframe(args.inputDir)
    xml_df.to_csv(args.outputFile, index=None)
    print("Successfully converted xml to csv.")
    if args.labelMapDir:
        os.makedirs(args.labelMapDir, exist_ok=True)
        label_map_path = os.path.join(args.labelMapDir, "label_map.pbtxt")
        print("Generate `{}`".format(label_map_path))

        # Create the `label_map.pbtxt` file
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


if __name__ == "__main__":
    main()
