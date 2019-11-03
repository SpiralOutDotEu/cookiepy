from unittest.mock import patch
import unittest
from unittest import mock
import cookiepy as cp
import xml.etree.ElementTree as ET


class mock_tree():
    def getroot(self):
        return "getroot"


def mock_parse(self):
    return mock_tree()


class TestXML_to_CSV(unittest.TestCase):

    @mock.patch('xml.etree.ElementTree.parse', side_effect=mock_parse)
    def test_it_converts_XML_to_element(self, mock_parse):
        result_tree, result_root = cp.xml_to_element("mock file")
        assert result_tree.getroot() == result_root == "getroot"
