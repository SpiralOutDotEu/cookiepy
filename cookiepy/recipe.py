from .xml_to_csv import *


def prepare_training_data(image_folder='images', data_folder='data'):
    objects_dataframe = xml_to_dataframe(image_folder)
    write_label_map(objects_dataframe, os.path.join(data_folder, 'train data/label_map.pbtxt'))
    train_dataframe, test_dataframe = split_train_test_dataframes(objects_dataframe)
    dataframe_to_csv(train_dataframe, os.path.join(data_folder, 'train data/train.csv'))
    dataframe_to_csv(test_dataframe, os.path.join(data_folder, 'train data/test.csv'))
