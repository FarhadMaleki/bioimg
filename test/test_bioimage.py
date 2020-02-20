import unittest
import matplotlib.pyplot as plt
import SimpleITK as sitk
import numpy as np

from bioimage import BioImage
from constants import Modality
from utils import visualize_slice


class TestBioImage(unittest.TestCase):
    def setUp(self):
        WIDTH = 10
        HEIGHT = 9
        DEPTH = 8
        self.dummy_data = np.array([np.array([np.arange(WIDTH) * i
                                              for i in range(HEIGHT)]) * k
                                    for k in range(DEPTH)])

    def test_load_preserves_shape_of_simple_images(self):
        # Test using dummy data
        image_address = 'test/data/dummy_image.{}'

        for ext in ['nrrd', 'nii']:
            address = image_address.format(ext)
            bioimage = BioImage(modality=Modality.SIMPLE_IMAGE, source=address)
            sitk_image = bioimage.load()
            voxels = sitk.GetArrayFromImage(sitk_image)
            self.assertTrue(np.array_equal(voxels, self.dummy_data))
        # Test using real data
        image_address = 'test/data/brain1_image.{}'
        IMAGE_SHAPE = (25, 256, 256)
        for ext in ['nrrd', 'nii']:
            address = image_address.format(ext)
            bioimage = BioImage(modality=Modality.SIMPLE_IMAGE, source=address)
            sitk_image = bioimage.load()
            voxels = sitk.GetArrayFromImage(sitk_image)
            self.assertEqual(voxels.shape, IMAGE_SHAPE)

    def test_load_preserves_shape_of_DICOM_images(self):
        address = 'test/data/dummy_image'
        bioimage = BioImage(modality=Modality.DICOM_CT_DIR, source=address)
        sitk_image = bioimage.load()
        voxels = sitk.GetArrayFromImage(sitk_image)
        self.assertTrue(np.array_equal(voxels, self.dummy_data))

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content_of_DICOM_images(self):
        brain1_image = 'test/data/brain1_image'
        brain1_label = 'test/data/brain1_label'
        brain1_ct = BioImage(brain1_image, modality=Modality.DICOM_CT_DIR)
        brain1_mask = BioImage(brain1_label, modality=Modality.DICOM_CT_DIR)
        brain1_image_array = sitk.GetArrayFromImage(brain1_ct.load())
        brain1_label_array = sitk.GetArrayFromImage(brain1_mask.load())
        location, width = 40, 400
        idx = 11
        fig, ax = plt.subplots()
        visualize_slice(brain1_image_array[idx],
                        brain1_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content_of_NRRD_files(self):
        brain1_image = 'test/data/brain1_image.nrrd'
        brain1_label = 'test/data/brain1_label.nrrd'
        brain1_ct = BioImage(brain1_image, modality=Modality.SIMPLE_IMAGE)
        brain1_mask = BioImage(brain1_label, modality=Modality.SIMPLE_IMAGE)
        brain1_image_array = sitk.GetArrayFromImage(brain1_ct.load())
        brain1_label_array = sitk.GetArrayFromImage(brain1_mask.load())
        location, width = 40, 400
        idx = 11
        fig, ax = plt.subplots()
        visualize_slice(brain1_image_array[idx],
                        brain1_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()

    @unittest.skip('Requires visual validation.')
    def test_load_preserves_content_of_a_DICOM_slice(self):
        brain1_image = 'test/data/brain1_image_slice11.dcm'
        brain1_label = 'test/data/brain1_label_slice11.dcm'
        brain1_ct = BioImage(brain1_image, modality=Modality.DICOM_CT_SLICE)
        brain1_mask = BioImage(brain1_label, modality=Modality.DICOM_CT_SLICE)
        brain1_image_array = sitk.GetArrayFromImage(brain1_ct.load())
        brain1_label_array = sitk.GetArrayFromImage(brain1_mask.load())
        location, width = 40, 400
        idx = 0
        fig, ax = plt.subplots()
        visualize_slice(brain1_image_array[idx],
                        brain1_label_array[idx],
                        ax, location, width, cmap='gray')
        plt.show()
