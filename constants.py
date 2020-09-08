class Modality(object):
    """
    DICOM_CT_DIR: Used for DICOM files within a directory.
    SIMPLE_IMAGE: Used for a single file supported by SimpleITK.
        See the supported files at the following link:
        https://simpleitk.readthedocs.io/en/master/IO.html
    DICOM_CT_SLICE: Used for a single slice from a DICOM
        file. File extension must be '.dcm' or '.DCM'.
    """
    DICOM_CT_DIR = 'DICOM_CT_DIR'
    SIMPLE_IMAGE = 'SIMPLE_IMAGE'
    DICOM_CT_SLICE = 'DICOM_CT_SLICE'
