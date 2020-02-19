""" Include the object used for reading different file formats.

"""
import os
import SimpleITK as sitk

from constants import BioImageModality
from utils import read_DICOM_CT_from_dir


class BioImage(object):
    """ Object used for reading biomedical images of different formats.

    Args:
        source: The source from which a biomedical image should be read.
        modality: A BioImageModality value 
    """
    def __init__(self, source, modality=None):
        BioImage.__validate(source, modality)
        self.modality = modality
        self.source = source

    @staticmethod
    def __validate(source, modality):
        """ Validate the source used for a given modality.
        Args:
            source: The source from which a biomedical image should be read.
            modality: A BioImageModality value. All supported
                modalities should be validated.
        Raises:
            ValueError: If the source or modality is not supported. See the
                supported modalities.
        """
        if modality == BioImageModality.DICOM_CT_DIR:
            assert os.path.isdir(source)
        elif modality == BioImageModality.NRRD_CT:
            assert os.path.isfile(source)
            assert source.lower().endswith('.nrrd')
        elif modality == BioImageModality.DICOM_CT_SLICE:
            assert os.path.isfile(source)
            assert source.lower().endswith('.dcm')
        else:
            raise ValueError('Invalid source or modality. See the supported '
                             'modalities.')

    def load(self):
        """ Load voxel values for a biomedical image.

        Returns:
            A SimpleITK.Image.

        """
        modality_to_load_function_map = {
            BioImageModality.DICOM_CT_DIR: BioImage.load_dicom_ct_from_dir,
            BioImageModality.NRRD_CT: BioImage.load_nrrd_ct_from_file,
            BioImageModality.DICOM_CT_SLICE: BioImage.load_dicom_ct_slice_from_file,
        }
        load_function = modality_to_load_function_map.get(self.modality)
        if load_function:
            return load_function(self.source)

        raise ValueError('Undefined modality.')

    @classmethod
    def load_dicom_ct_from_dir(cls, dir_path):
        """ Load a CT image (or its contours) from a directory.
        Args:
            dir_path (str): Address of the directory containing the DICOM files.

        Returns:
            A SimpleITK image.
        """
        if not os.path.isdir(dir_path):
            raise ValueError('path must be a directory address, but it is not'
                             'Check {}'.format(dir_path))
        image = read_DICOM_CT_from_dir(dir_path)
        return image

    @classmethod
    def load_nrrd_ct_from_file(cls, file_path):
        """ Load a CT image (or its contours) from an NRRD file.
        Args:
            file_path (str): Address of an NRRD file.

        Returns:
            A SimpleITK image.
        """
        image = sitk.ReadImage(file_path)
        return image

    @classmethod
    def load_dicom_ct_slice_from_file(cls, file_path):
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
