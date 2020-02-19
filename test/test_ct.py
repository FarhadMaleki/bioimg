import unittest
import SimpleITK as sitk
import matplotlib.pyplot as plt
from ct import DICOMCTDIR
from ct import NRRDCT
from utils import visualize_slice


class TestNRRDCT(unittest.TestCase):
    def setUp(self):
        self.brain1_image_path = 'test/data/brain1_image.nrrd'
        self.brain1_label_path = 'test/data/brain1_label.nrrd'
        self.brain1_masked_ct = NRRDCT('brain1', 'CT1', self.brain1_image_path,
                                       mask_path=self.brain1_label_path)
        self.brain1_unmasked_ct = NRRDCT('brain1', 'CT1',
                                         self.brain1_image_path,
                                         mask_path=None)
        self.brain1_dims = (25, 256, 256)

    def test_load(self):
        brain1_image, brain1_label = self.brain1_masked_ct.load()
        self.assertTrue(isinstance(brain1_image, sitk.Image))
        self.assertTrue(isinstance(brain1_label, sitk.Image))
        self.assertEqual(NRRDCT.get_array(brain1_image).shape,
                         self.brain1_dims)
        self.assertEqual(NRRDCT.get_array(brain1_label).shape,
                         self.brain1_dims)

        brain1_image, brain1_label = self.brain1_unmasked_ct.load()
        self.assertIsInstance(brain1_image, sitk.Image)
        self.assertIsNone(brain1_label)
        self.assertEqual(NRRDCT.get_array(brain1_image).shape,
                         self.brain1_dims)
        # Check sample_id and image_id assignment
        self.assertEqual(self.brain1_masked_ct.sample_id, 'brain1')
        self.assertEqual(self.brain1_masked_ct.image_id, 'CT1')

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content(self):
        brain1_image, brain1_label = self.brain1_masked_ct.load()
        brain1_image_array = NRRDCT.get_array(brain1_image)
        brain1_label_array = NRRDCT.get_array(brain1_label)
        location, width = 40, 400
        idx = 11
        fig, ax = plt.subplots()
        visualize_slice(brain1_image_array[idx],
                        brain1_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()


class TestDICOMCTDIR(unittest.TestCase):
    def setUp(self):
        self.brain1_image_path = 'test/data/brain1_image'
        self.brain1_label_path = 'test/data/brain1_label'
        self.brain1_masked_ct = DICOMCTDIR('brain1', 'CT1',
                                           self.brain1_image_path,
                                           mask_path=self.brain1_label_path)
        self.brain1_unmasked_ct = DICOMCTDIR('brain1', 'CT1',
                                             self.brain1_image_path,
                                             mask_path=None)
        self.brain1_dims = (25, 256, 256)

    def test_load(self):
        brain1_image, brain1_label = self.brain1_masked_ct.load()
        self.assertTrue(isinstance(brain1_image, sitk.Image))
        self.assertTrue(isinstance(brain1_label, sitk.Image))
        self.assertEqual(NRRDCT.get_array(brain1_image).shape,
                         self.brain1_dims)
        self.assertEqual(NRRDCT.get_array(brain1_label).shape,
                         self.brain1_dims)

        brain1_image, brain1_label = self.brain1_unmasked_ct.load()
        self.assertIsInstance(brain1_image, sitk.Image)
        self.assertIsNone(brain1_label)
        self.assertEqual(NRRDCT.get_array(brain1_image).shape,
                         self.brain1_dims)
        # Check sample_id and image_id assignment
        self.assertEqual(self.brain1_masked_ct.sample_id, 'brain1')
        self.assertEqual(self.brain1_masked_ct.image_id, 'CT1')

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content(self):
        brain1_image, brain1_label = self.brain1_masked_ct.load()
        brain1_image_array = NRRDCT.get_array(brain1_image)
        brain1_label_array = NRRDCT.get_array(brain1_label)
        location, width = 40, 400
        idx = 11
        fig, ax = plt.subplots()
        visualize_slice(brain1_image_array[idx],
                        brain1_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()
