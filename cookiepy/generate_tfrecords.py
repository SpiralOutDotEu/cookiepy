import os
import io
import pandas as pd
import tensorflow as tf
from .od_methods import DatasetUtilInterface as dataset_util_interface
from .od_methods import LabelMapUtilInterface as label_map_util_interface
from PIL import Image
from collections import namedtuple, OrderedDict


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path, label_map, dataset_util_interface):
    with tf.gfile.GFile(os.path.join(path, "{}".format(group.filename)), "rb") as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode("utf8")
    image_format = b"jpg"
    # check if the image format is matching with your images.
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row["xmin"] / width)
        xmaxs.append(row["xmax"] / width)
        ymins.append(row["ymin"] / height)
        ymaxs.append(row["ymax"] / height)
        classes_text.append(row["class"].encode("utf8"))
        class_index = label_map.get(row["class"])
        assert (
            class_index is not None
        ), "class label: `{}` not found in label_map: {}".format(
            row["class"], label_map
        )
        classes.append(class_index)

    tf_example = tf.train.Example(
        features=tf.train.Features(
            feature={
                "image/height": dataset_util_interface.int64_feature(height),
                "image/width": dataset_util_interface.int64_feature(width),
                "image/filename": dataset_util_interface.bytes_feature(filename),
                "image/source_id": dataset_util_interface.bytes_feature(filename),
                "image/encoded": dataset_util_interface.bytes_feature(encoded_jpg),
                "image/format": dataset_util_interface.bytes_feature(image_format),
                "image/object/bbox/xmin": dataset_util_interface.float_list_feature(xmins),
                "image/object/bbox/xmax": dataset_util_interface.float_list_feature(xmaxs),
                "image/object/bbox/ymin": dataset_util_interface.float_list_feature(ymins),
                "image/object/bbox/ymax": dataset_util_interface.float_list_feature(ymaxs),
                "image/object/class/text": dataset_util_interface.bytes_list_feature(
                    classes_text
                ),
                "image/object/class/label": dataset_util_interface.int64_list_feature(classes),
            }
        )
    )
    return tf_example


def csv_to_tfrecord(image_folder, label_map, csv_input, output_path, dataset_util_interface, label_map_util_interface):
    dirname = os.path.dirname(output_path)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    path = image_folder
    examples = pd.read_csv(csv_input)

    writer = tf.python_io.TFRecordWriter(output_path)
    label_map = label_map_util_interface.load_labelmap(label_map)
    categories = label_map_util_interface.convert_label_map_to_categories(
        label_map, max_num_classes=90, use_display_name=True
    )
    category_index = label_map_util_interface.create_category_index(categories)
    label_map = {}
    for k, v in category_index.items():
        label_map[v.get("name")] = v.get("id")
    grouped = split(examples, "filename")
    for group in grouped:
        tf_example = create_tf_example(group, path, label_map, dataset_util_interface)
        writer.write(tf_example.SerializeToString())
    writer.close()

    print("Successfully created the TFRecords: {}".format(output_path))
