""" Include the object used for reading different file formats.

"""
import os
import SimpleITK as sitk

from constants import Modality
from utils import read_DICOM_from_dir


class BioImage(object):
    """ Object used for reading biomedical images of different formats.

    Args:
        source: The source from which a biomedical image should be read.
        modality: A BioImageModality value 
    """
    def __init__(self, source, modality=None):
        self.source = source
        self.modality = modality

    def load(self):
        """ Load voxel values for an image.

        Returns:
            A SimpleITK.Image.

        """
        modality_to_load_function_map = {
            Modality.DICOM_CT_DIR: BioImage.load_dicom_from_dir,
            Modality.SIMPLE_IMAGE: BioImage.load_simple_image_from_file,
            Modality.DICOM_CT_SLICE: BioImage.load_dicom_slice_from_file,
        }
        load_function = modality_to_load_function_map.get(self.modality)
        if load_function:
            return load_function(self.source)

        raise ValueError('Undefined modality.')

    @classmethod
    def load_dicom_from_dir(cls, dir_path):
        """ Load an image (or its contours) from a directory.
        Args:
            dir_path (str): Address of the directory containing the DICOM files.

        Returns:
            A SimpleITK image.
        """
        if not os.path.isdir(dir_path):
            msg = '{} must be a directory address, but it is not.'
            raise ValueError(msg.format(dir_path))
        image = read_DICOM_from_dir(dir_path)
        return image

    @classmethod
    def load_simple_image_from_file(cls, file_path):
        """ Load an image (or its contours) from a file.

        File types that can be read by SimpleITK.ReadImage are supported.

        Args:
            file_path (str): Address of the image file.

        Returns:
            A SimpleITK image.
        """
        image = sitk.ReadImage(file_path)
        return image

    @classmethod
    def load_dicom_slice_from_file(cls, file_path):
        """ Load a slice of a CT image (or its contours) from a DICOM file.
        Args:
            file_path (str): Address of an DICOM file.

        Returns:
            A SimpleITK image.
        """
        return sitk.ReadImage(file_path)

    def __str__(self):
        """ A string representation of a BioImage object.

        Returns:
            A string representing modality and source.

        """
        return 'Modality: {}, Source: {} '.format(self.modality, self.source)
