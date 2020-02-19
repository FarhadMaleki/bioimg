""" Module for working with CT Data.

"""
import SimpleITK as sitk
from bioimage import BioImage
from constants import BioImageModality


class DICOMCTDIR(object):
    """ Create a DICOM CT object from a directory for the CT image
        (and possibly a directory for the image contours).

    Args:
        sample_id (str): An identifier assigned to each sample,
            i.e. each patient.
        image_id (str): An identifier assigned to each image,
            i.e. each CT image.
        image_path (str): The address of the directory containing DICOM
            files for the CT.
        mask_path (str): The address of the directory containing DICOM
            files for the contour.
    """
    MODALITY = BioImageModality.DICOM_CT_DIR

    def __init__(self, sample_id, image_id, image_path, mask_path=None):
        self.sample_id = sample_id
        self.image_id = image_id
        self.image = BioImage(image_path, modality=DICOMCTDIR.MODALITY)
        self.mask = None
        if mask_path is not None:
            self.mask = BioImage(mask_path, modality=DICOMCTDIR.MODALITY)

    @classmethod
    def get_array(cls, image):
        """ Get the voxel values for either the CT image or its mask.

        Args:
            image (DICOMCTDIR): The object for which the voxel values
                are extracted.

        Returns:
            A numpy array containing the voxel values.
        """
        return sitk.GetArrayViewFromImage(image)

    def load(self):
        """ Loads the data for CT image data (and possibly the contour data
            for the contours)

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
                ValueError('CT and its Mask must be of the same shape')
        return image, mask


class NRRDCT(object):
    """ Create a NRRD CT object from a nrrd file for the CT image
            (and possibly a nrrd file for the image contours).

        Args:
            sample_id (str): An identifier assigned to each sample,
                i.e. each patient.
            image_id (str): An identifier assigned to each image,
                i.e. each CT image.
            image_path (str): The address of the nrrd file for the CT.
            mask_path (str): The address of the nrrd file for the contour.
        """
    MODALITY = BioImageModality.NRRD_CT

    def __init__(self, sample_id, image_id, image_path, mask_path=None):
        self.sample_id = sample_id
        self.image_id = image_id
        self.image = BioImage(image_path, modality=NRRDCT.MODALITY)
        self.mask = None
        if mask_path is not None:
            self.mask = BioImage(mask_path, modality=NRRDCT.MODALITY)

    @classmethod
    def get_array(cls, image):
        """ Get the voxel values for either the CT image or its mask.

        Args:
            image (DICOMCTDIR): The object for which the voxel values
                are extracted.

        Returns:
            A numpy array containing the voxel values.
        """
        return sitk.GetArrayFromImage(image)

    def load(self):
        """ Loads the data for CT image data (and possibly the contour data
            for the contours)

        Returns:
            image vexel values as a numpy array.
            contour voxel values as a numpy array.
        """
        image = self.image.load()
        mask = None
        if self.mask is not None:
            mask = self.mask.load()
            image_shape = (NRRDCT.get_array(image)).shape
            mask_shape = (NRRDCT.get_array(mask)).shape
            if image_shape != mask_shape:
                ValueError('CT and its Mask must be of the same shape')
        return image, mask
