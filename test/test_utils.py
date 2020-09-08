import json
import unittest
from collections import OrderedDict
from utils import read_catalog
from utils import partition
from ct import DICOMCTDIR
from ct import SimpleImage


class TestUtilsMethods(unittest.TestCase):

    def test_read_catalog(self):
        catalog_file_path = 'test/data/catalog.csv'
        catalog_sequence = read_catalog(catalog_file_path, sep=',')
        expected = [["brain1", "CT1", "test/data/brain1_image",
                     "test/data/brain1_label"],
                    ["brain2", "CT1", "test/data/brain1_image",
                     "test/data/brain1_label"]]
        for x, y in zip(catalog_sequence, expected):
            self.assertListEqual(x, y)
        # Read a catalog with no mask
        catalog_file_path = 'test/data/catalog_unmasked.csv'
        catalog_sequence = read_catalog(catalog_file_path, sep=',')
        expected = [["brain1", "CT1", "test/data/brain1_image", ''],
                    ["brain2", "CT1", "test/data/brain1_image", '']]
        for x, y in zip(catalog_sequence, expected):
            self.assertListEqual(x, y)

    def test_partition_with_zero_indexed_elements(self):
        x = list(range(10))
        parts = partition(x, [0.5, 0.5])
        self.assertEqual(len(parts[0]), 5)
        self.assertEqual(len(parts[1]), 5)
        self.assertEqual(set(parts[0]).union(set(parts[1])), set(x))

    def test_partition_with_char_elements(self):
        # An array with 10 items
        x = list(['R', 'A', 'N', 'D', 'O', 'M', 'T', 'E', 'S', 'T'])
        parts = partition(x, [0.2, 0.8])
        self.assertEqual(len(parts[0]), 2)
        self.assertEqual(len(parts[1]), 8)
        self.assertEqual(set(parts[0]).union(set(parts[1])), set(x))
