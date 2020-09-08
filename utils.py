""" This module contains utility functions.

"""
import random
import numpy as np
import SimpleITK as sitk



def visualize_slice(image, mask, ax, location, width, **kwargs):
    """ Visualize a slice of a 3D numpy array.

    Args:
        image: A 3D numpy array.
        mask: A 3D numpy array.
        ax: An Axis object to be used for drawing.
        location: Center point in Hounsfield unit for the observation window.
        width: Width of the observation window in Hounsfield unit.
        **kwargs: Other graphical parameters used for drawing.

    """
    radious = width // 2
    min_voxel, max_voxel = location - radious, location + radious
    img = image.copy()
    img[img < min_voxel] = min_voxel
    img[img > max_voxel] = max_voxel
    ax.imshow(img, interpolation='none', **kwargs)
    if mask is not None:
        mask_image = np.ma.masked_where(mask == 0, mask)
        ax.imshow(mask_image, cmap='autumn', interpolation='none', alpha=0.7)


def read_DICOM_from_dir(dir_path):
    """ Read a CT image (or its contours) from a directory.

    Args:
        dir_path (str): Address of the directory containing DICOM files.

    Returns: A SimpleITK.Image.

    """
    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(dir_path)
    if len(series_ids) == 0:
        raise ValueError('No DICOM file in directory:\n{}'.format(dir_path))
    slice_paths = reader.GetGDCMSeriesFileNames(dir_path, series_ids[0])
    reader.SetFileNames(slice_paths)
    ct = reader.Execute()
    # Reading matadata from one slice, currently SimpleITK does not support
    # extracting metadata when reading a series
    reader = sitk.ImageFileReader()
    reader.SetFileName(slice_paths[0])
    img = reader.Execute()
    for k in img.GetMetaDataKeys():
        value = img.GetMetaData(k)
        ct.SetMetaData(k, value)
    return ct


def read_catalog(catalog_file_path, sep=','):
    """ Read a Catalog file.
    A Catalog file is a tabular file containing 4 columns. These are
        (1) sample_id, (2) image_id, (3) image_src, and (4) mask_src,
        respectively.

    Args:
        catalog_file_path: Address of a catalog file.
        sep: A field seperator.

    Returns:
        return a list of lists, where each internal list contain for elements:
            (1) sample_id, (2) image_id, (3) image_src, and (4) mask_src.

    """
    data_sequence = []
    with open(catalog_file_path) as fin:
        for line in fin:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            instance_info = [x.strip() for x in line.split(sep)]
            data_sequence.append(instance_info)
    return data_sequence


def partition(elements, portions):
    """ partitions samples randomly.

    Args:
        elements: A list.
        portions: A list of positive real numbers, each between 0 and 1,
            exclusively. The summation of elements in portions must be 1.

    Returns:
        A random partition of samples, where partitions[i] includes
            portions[i] * 100 percent of samples.

    """
    assert sum(portions) == 1
    index_value_map = {idx: value for idx, value in enumerate(elements)}
    random_indices = list(index_value_map.keys())
    random.shuffle(random_indices)
    partitions = []
    total = 0
    start = 0
    for i in range(len(portions) - 1):
        num_elements = int(portions[i] * len(elements))
        total += num_elements
        partition_indices = random_indices[start: total]
        partitions.append([index_value_map[idx] for idx in partition_indices])
    partition_indices = random_indices[total:]
    partitions.append([index_value_map[idx] for idx in partition_indices])
    return partitions
