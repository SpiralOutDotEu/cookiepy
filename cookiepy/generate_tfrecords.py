# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf
from .od_methods import DuInterface as du_interface
from .od_methods import LmInterface as lm_interface
from PIL import Image
from collections import namedtuple,OrderedDict




# if your image has more labels input them as
# flags.DEFINE_string('label0', '', 'Name of class[0] label')
# flags.DEFINE_string('label1', '', 'Name of class[1] label')
# and so on.




# TO-DO replace this with label map
# for multiple labels add more else if statements
def class_text_to_int(row_label):
    if row_label == FLAGS.label:  # 'ship':
        return 1
    # comment upper if statement and uncomment these statements for multiple labelling
    # if row_label == FLAGS.label0:
    #   return 1
    # elif row_label == FLAGS.label1:
    #   return 0
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path, label_map, du_interface):
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
                "image/height": du_interface.int64_feature(height),
                "image/width": du_interface.int64_feature(width),
                "image/filename": du_interface.bytes_feature(filename),
                "image/source_id": du_interface.bytes_feature(filename),
                "image/encoded": du_interface.bytes_feature(encoded_jpg),
                "image/format": du_interface.bytes_feature(image_format),
                "image/object/bbox/xmin": du_interface.float_list_feature(xmins),
                "image/object/bbox/xmax": du_interface.float_list_feature(xmaxs),
                "image/object/bbox/ymin": du_interface.float_list_feature(ymins),
                "image/object/bbox/ymax": du_interface.float_list_feature(ymaxs),
                "image/object/class/text": du_interface.bytes_list_feature(
                    classes_text
                ),
                "image/object/class/label": du_interface.int64_list_feature(classes),
            }
        )
    )
    return tf_example


def csv_to_tfrecord(image_folder, label_map, csv_input, output_path, du_interface, lm_interface):
    dirname = os.path.dirname(output_path)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    writer = tf.python_io.TFRecordWriter(output_path)
    
    path = image_folder
    examples = pd.read_csv(csv_input)

    label_map = lm_interface.load_labelmap(label_map)
    categories = lm_interface.convert_label_map_to_categories(
        label_map, max_num_classes=90, use_display_name=True
    )
    category_index = lm_interface.create_category_index(categories)
    label_map = {}
    for k, v in category_index.items():
        label_map[v.get("name")] = v.get("id")
    
    grouped = split(examples, "filename")
    for group in grouped:
        tf_example = create_tf_example(group, path, label_map, du_interface)
        writer.write(tf_example.SerializeToString())
    
    writer.close()
    
    print("Successfully created the TFRecords: {}".format(output_path))









