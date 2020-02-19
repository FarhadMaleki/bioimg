import unittest
import matplotlib.pyplot as plt
import SimpleITK as sitk

from constants import BioImageModality
from utils import visualize_slice
from bioimage import BioImage


class TestBioImage(unittest.TestCase):
    def setUp(self):
        # Load a CT image in NRRD format
        self.brain1_image = 'test/data/brain1_image.nrrd'
        self.brain1_label = 'test/data/brain1_label.nrrd'
        self.brain1_ct = BioImage(self.brain1_image, modality=BioImageModality.NRRD_CT)
        self.brain1_mask = BioImage(self.brain1_label, modality=BioImageModality.NRRD_CT)
        self.brain1_image_array = sitk.GetArrayFromImage(self.brain1_ct.load())
        brain1_label_array = sitk.GetArrayFromImage(self.brain1_mask.load())
        self.brain1_label_array = brain1_label_array
        self.brain1_dims = (25, 256, 256)

        # Load a CT in DICOM format
        self.brain1_image = 'test/data/brain1_image'
        self.brain1_label = 'test/data/brain1_label'
        self.brain1_ct = BioImage(self.brain1_image, modality=BioImageModality.DICOM_CT_DIR)
        self.brain1_mask = BioImage(self.brain1_label, modality=BioImageModality.DICOM_CT_DIR)
        self.brain1_image_array = sitk.GetArrayFromImage(self.brain1_ct.load())
        self.brain1_label_array = sitk.GetArrayFromImage(self.brain1_mask.load())
        self.brain1_dims = (25, 256, 256)

        # Load a single slice CT in DICOM format
        self.brain1_slice_image = 'test/data/brain1_image_slice11.dcm'
        self.brain1_slice_label = 'test/data/brain1_label_slice11.dcm'
        self.brain1_slice_ct = BioImage(self.brain1_slice_image,
                                        modality=BioImageModality.DICOM_CT_SLICE)
        self.brain1_slice_mask = BioImage(self.brain1_slice_label,
                                          modality=BioImageModality.DICOM_CT_SLICE)
        temp = sitk.GetArrayFromImage(self.brain1_slice_ct.load())
        self.brain1_slice_image_array = temp
        temp = sitk.GetArrayFromImage(self.brain1_slice_mask.load())
        self.brain1_slice_label_array = temp
        self.brain1_slice_dims = (1, 256, 256)

    def test_load_preserves_shape_of_NRRD_files(self):
        self.assertEqual(self.brain1_image_array.shape, self.brain1_dims)

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content_of_NRRD_files(self):
        location, width = 40, 400
        idx = 11
        fig, ax = plt.subplots()
        visualize_slice(self.brain1_image_array[idx],
                        self.brain1_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()

    def test_load_preserve_shape_of_NRRD_fiels(self):
        self.assertEqual(self.brain1_image_array.shape, self.brain1_dims)

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content_of_DICOM_dir(self):
        location, width = 40, 400
        idx = 11
        fig, ax = plt.subplots()
        visualize_slice(self.brain1_image_array[idx],
                        self.brain1_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()

    def test_load_preserve_shape_of_single_dicom_slice_fiels(self):
        self.assertEqual(self.brain1_slice_image_array.shape,
                         self.brain1_slice_dims)

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content_of_DICOM_dir(self):
        location, width = 40, 400
        idx = 0
        fig, ax = plt.subplots()
        visualize_slice(self.brain1_slice_image_array[idx],
                        self.brain1_slice_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()
