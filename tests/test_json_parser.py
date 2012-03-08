__author__ = 'lchang'

import unittest
from utils import json_parser

class TestJsonParser(unittest.TestCase):


    def setUp(self):
        self.json_obj = {'key_1':'value_1', 'key_2':'value_2'}

    def test_parse_json(self):
        #parse the json and split values and keys
        parser = json_parser.JsonParser()
        json_list = [['key_1', 'key_2'], ['value_1', 'value_2']]
        keys = parser.parse_json(self.json_obj)
        self.assertEqual(keys, json_list)


if __name__ == '__main__':
    unittest.main()
