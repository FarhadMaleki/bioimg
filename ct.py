""" This module provide functionality for working masked or unmasked images.

"""
import SimpleITK as sitk
from bioimage import BioImage
from constants import Modality


class DICOMCTDIR(object):
    """ Create an object from a directory containing DICOM files.

        For masked images, the address of a second directory containg masks
            must be provided.

    Args:
        sample_id (str): An identifier assigned to each sample,
            i.e. each patient.
        image_id (str): An identifier assigned to each image,
        image_path (str): The address of the directory containing DICOM
            files.
        mask_path (str): The address of the directory containing DICOM
            files for the image mask. Default is None for images with no mask.
    """
    MODALITY = Modality.DICOM_CT_DIR

    def __init__(self, sample_id, image_id, image_path, mask_path=None):
        self.sample_id = sample_id
        self.image_id = image_id
        self.image = BioImage(image_path, modality=DICOMCTDIR.MODALITY)
        self.mask = None
        if mask_path is not None:
            self.mask = BioImage(mask_path, modality=DICOMCTDIR.MODALITY)

    @classmethod
    def get_array(cls, image):
        """ Get the voxel values.

        Args:
            image (DICOMCTDIR): The object for which the voxel values
                are extracted.

        Returns:
            A numpy array containing the voxel values.
        """
        return sitk.GetArrayViewFromImage(image)

    def load(self):
        """ Loads the data for an image and its mask, if applicable.

        Returns:
            image vexel values as a numpy array.
            contour voxel values as a numpy array.
        """
        image = self.image.load()
        mask = None
        if self.mask is not None:
            mask = self.mask.load()
            image_shape = (DICOMCTDIR.get_array(image)).shape
            mask_shape = (DICOMCTDIR.get_array(mask)).shape
            if image_shape != mask_shape:
                ValueError('Image and its mask must be of the same shape')
        return image, mask


class SimpleImage(object):
    """ Create a SimpleImage object.

    For unmasked images, a single file is required. For masked images two
        files, one for the image and another for the mask, are required.

    Args:
        sample_id (str): An identifier assigned to each sample,
            i.e. each patient.
        image_id (str): An identifier assigned to each image.
        image_path (str): The address of the image file.
        mask_path (str): The address of the mask file.
        """
    MODALITY = Modality.SIMPLE_IMAGE

    def __init__(self, sample_id, image_id, image_path, mask_path=None):
        self.sample_id = sample_id
        self.image_id = image_id
        self.image = BioImage(image_path, modality=SimpleImage.MODALITY)
        self.mask = None
        if mask_path is not None:
            self.mask = BioImage(mask_path, modality=SimpleImage.MODALITY)

    @classmethod
    def get_array(cls, image):
        """ Get the voxel values.

        Args:
            image (DICOMCTDIR): The object for which the voxel values
                are extracted.

        Returns:
            A numpy array containing the voxel values.
        """
        return sitk.GetArrayFromImage(image)

    def load(self):
        """ Loads voxel values for the image and its mask, if applicable.

        Returns:
            image vexel values as a numpy array.
            contour voxel values as a numpy array.
        """
        image = self.image.load()
        mask = None
        if self.mask is not None:
            mask = self.mask.load()
            image_shape = (SimpleImage.get_array(image)).shape
            mask_shape = (SimpleImage.get_array(mask)).shape
            if image_shape != mask_shape:
                ValueError('Image and its mask must be of the same shape')
        return image, mask
