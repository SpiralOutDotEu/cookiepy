
class DatasetUtilInterface():

    def int64_feature(value):
        raise NotImplementedError

    def int64_list_feature(value):
        raise NotImplementedError

    def bytes_feature(value):
        raise NotImplementedError

    def bytes_list_feature(value):
        raise NotImplementedError

    def float_list_feature(value):
        raise NotImplementedError

    def load_labelmap(path):
        raise NotImplementedError


class LabelMapUtilInterface():

    def _validate_label_map(label_map):
        raise NotImplementedError

    def create_category_index(categories):
        raise NotImplementedError

    def get_max_label_map_index(label_map):
        raise NotImplementedError

    def convert_label_map_to_categories(label_map,
                                        max_num_classes,
                                        use_display_name=True):
        raise NotImplementedError

    def load_labelmap(path):
        raise NotImplementedError

    def get_label_map_dict(label_map_path_or_proto,
                           use_display_name=False,
                           fill_in_gaps_and_background=False):
        raise NotImplementedError

    def create_categories_from_labelmap(label_map_path, use_display_name=True):
        raise NotImplementedError

    def create_category_index_from_labelmap(label_map_path, use_display_name=True):
        raise NotImplementedError

    def create_class_agnostic_category_index(self):
        raise NotImplementedError
