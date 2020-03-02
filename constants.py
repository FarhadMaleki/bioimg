class Modality(object):
    """
    DICOM_CT_DIR: Used for DICOM files within a directory.
    NRRD_CT: Used for an NRRD file. File extensions must be
        '.nrrd' or '.NRRD'.
    DICOM_CT_SLICE: Used for a single slice from a DICOM
        file. File extension must be '.dcm' or '.DCM'.
    """
    DICOM_CT_DIR = 'DICOM_CT_DIR'
    SIMPLE_IMAGE = 'SIMPLE_IMAGE'
    DICOM_CT_SLICE = 'DICOM_CT_SLICE'
