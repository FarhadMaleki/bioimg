import json
import unittest
from collections import OrderedDict
from utils import HandCraft
from utils import dump_CT_2_hdf5
from utils import dump_radiomics_features_2_json
from utils import read_catalog
from utils import extract_radiomics_features
from utils import partition
from ct import DICOMCTDIR
from ct import NRRDCT


class TestHandCraft(unittest.TestCase):
    def setUp(self):
        brain1_image_path = 'test/data/brain1_image.nrrd'
        brain1_label_path = 'test/data/brain1_label.nrrd'
        brain1_masked_ct = NRRDCT('brain1', 'CT1', brain1_image_path,
                                  mask_path=brain1_label_path)
        self.brain1_image, self.brain1_mask = brain1_masked_ct.load()
        config_path = 'test/data/params.yaml'
        self.hc = HandCraft(config_path=config_path)

    def test_extract(self):
        features = self.hc.extract(self.brain1_image, self.brain1_mask)
        self.assertIsInstance(features, dict)
        self.assertNotEqual(len(features), 0)

    def test_hold(self):
        prefix = 'original_glcm'
        features = self.hc.extract(self.brain1_image, self.brain1_mask)
        features = HandCraft.hold(features, prefix=prefix)
        self.assertIsInstance(features, OrderedDict)
        for name in features.keys():
            self.assertTrue(name.startswith(prefix))


class TestUtilsMethods(unittest.TestCase):
    def test_dump_masked_CTs_2_hdf5(self):
        catalog_file_path = 'test/data/catalog.csv'
        dataset_file_path = 'test/data/temp.h5'
        dataset_id = 'Temporary_HDF5'
        dump_CT_2_hdf5(catalog_file_path,
                       dataset_file_path,
                       dataset_id,
                       CT=DICOMCTDIR,
                       mode='w',
                       sep=',')

    def test_dump_unmasked_CTs_2_hdf5(self):
        catalog_file_path = 'test/data/catalog_unmasked.csv'
        dataset_file_path = 'test/data/temp.h5'
        dataset_id = 'Temporary_HDF5'
        dump_CT_2_hdf5(catalog_file_path,
                       dataset_file_path,
                       dataset_id,
                       CT=DICOMCTDIR,
                       mode='w',
                       sep=',')

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

    def test_dump_radiomics_features_2_json(self):
        catalog_file_path = 'test/data/catalog.csv'
        json_file_path = 'test/data/radiomics_features_temp.json'
        config_path = 'test/data/params.yaml'
        features = extract_radiomics_features(catalog_file_path, config_path,
                                              CT=DICOMCTDIR, sep=',')
        dump_radiomics_features_2_json(json_file_path, catalog_file_path,
                                       config_path, CT=DICOMCTDIR, sep=',')
        with open(json_file_path) as fin:
            saved_features = json.load(fin)

        for (sample_id, image_id), expected_features in features.items():
            for k, expected in expected_features.items():
                observed = saved_features['{},{}'.format(sample_id,
                                                         image_id)][k]
                try:
                    # Check equality of noniterables
                    self.assertEqual(expected, observed)
                except:
                    # Check equality of iterables
                    self.assertSequenceEqual(expected, observed)

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
