from unittest.mock import patch, MagicMock
import unittest
from unittest import mock
from cookiepy.xml_to_csv import xml_to_element, all_object_elements_in, object_element_to_dict, dataframe_to_csv, \
    xml_to_dataframe
import xml.etree.ElementTree as ET


class MockTree:
    @staticmethod
    def getroot():
        return "getroot"


def mock_parse(self):
    return MockTree()


class TestItConvertsXMLtoCSV(unittest.TestCase):

    @mock.patch('xml.etree.ElementTree.parse', side_effect=mock_parse)
    def test_it_converts_XML_to_element(self, mock_parse):
        result_tree, result_root = xml_to_element("mock file")
        assert result_tree.getroot() == result_root == "getroot"

    def test_it_gets_object_elements_from_root(self):
        mock_root = MagicMock()
        mock_root.findall = MagicMock(return_value="mock_objects")
        result = all_object_elements_in(mock_root)
        assert result is "mock_objects"
        mock_root.findall.assert_called_with("object")

    def test_it_converts_object_element_to_dict(self):
        stub_root = ET.fromstring("<root>"
                                  "<folder>images</folder>"
                                  r"<path>C:\data\images\file.jpg</path>"
                                  "<filename>file.jpg</filename>"
                                  "<size><width>800</width><height>600</height></size>"
                                  "</root>")
        stub_object_element = ET.fromstring("<object><name>object1</name><pose>Unspecified</pose>"
                                            "<truncated>0</truncated><difficult>0</difficult>"
                                            "<bndbox><xmin>100</xmin><ymin>101</ymin>"
                                            "<xmax>200</xmax><ymax>201</ymax></bndbox></object>")
        result = object_element_to_dict(stub_root, stub_object_element)
        assert result == {"filename": "file.jpg",
                          "width": 800,
                          "height": 600,
                          "class": "object1",
                          "xmin": 100,
                          "ymin": 101,
                          "xmax": 200,
                          "ymax": 201}

    def test_it_saves_dataframe_to_csv(self):
        objects_dataframe = xml_to_dataframe('../data/labeled images')
        dataframe_to_csv(objects_dataframe, '../data/train data/train.csv')
        pass
        # mock_dataframe = MagicMock()
        # mock_file = MagicMock()
        # mock_dataframe.to_csv = MagicMock(return_value="mock_dataframe_to_csv")
        # dataframe_to_csv(mock_dataframe, mock_file)
        # mock_dataframe.to_csv.assert_called_with(mock_file, index=None)
