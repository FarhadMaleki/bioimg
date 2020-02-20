""" This module contains utility functions.

"""
import json
import random
from collections import OrderedDict

import yaml
import h5py
import numpy as np
import SimpleITK as sitk
from radiomics import featureextractor


class YAMLLoader(object):
    ''' Load parameters from a YAML file.

    Args:
        address (str): The address of the file containing parameters.
    '''
    def __init__(self, address):
        with open(address) as fin:
            self._params = yaml.load(fin, Loader=yaml.SafeLoader)

    @property
    def pars(self):
        ''' Return the parameters.

        Returns:
            A dictionary containing the parameters.
        '''
        return self._params


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


class HandCraft(object):
    def __init__(self, config_path):
        """ Instantiate an object for feature extraction.

        Args:
            config_path (stt): The path of config file, which should be a
            YAML or  JSON file. See the documentation of pyradiomics for
            information about the content of this file.
        """
        self.extractor = featureextractor.RadiomicsFeatureExtractor(config_path)

    def extract(self, image, mask):
        return self.extractor.execute(image, mask)

    @classmethod
    def hold(cls, features, prefix):
        """ Filter features and retain those with a name that matches prefix.

        For example a prefix of 'original_shape_' retain all shape features,
            a prefix of 'original_firstorder' retain all first order
            features, or a prefix of 'original_' retains all features.

        Args:
            features (OrderedDict: An OrderedDict of all features and general
               information.
            prefix (str): A string used to select all features that their
                names starts with that prefix.

        Returns:
            An OrderedDic, where the keys are sorted in an ascending order.

        """
        names = sorted([k for k in features.keys() if k.startswith(prefix)])
        remained = OrderedDict()
        for k in names:
            remained[k] = features[k]
        return remained


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



def dump_CT_2_hdf5(catalog_file_path, dataset_file_path, dataset_id,
                   CT, mode='w', sep=','):
    """ Dump a group of CT images and their contours to a HDF5 file

    Args:
        catalog_file_path (str):
        dataset_file_path (str):
        dataset_id (str):
        CT: A CT object such as DICOMCTDIR.
        mode: mode for dumping files to the HDF5 file, default is 'w'.
        sep: A field seperator for the catalog file.

    """
    # Build the data_sequence to define the images/masks
    data_sequence = read_catalog(catalog_file_path, sep)
    # Dump data to a HDF5 file
    with h5py.File(dataset_file_path, mode) as hdf:
        for (sample_id, image_id, image_src, mask_src) in data_sequence:
            if mask_src == '':
                mask_src = None
            instance = CT(sample_id, image_id, image_src, mask_src)
            image, mask = instance.load()
            key = '/{}/{}/{}'.format(dataset_id, sample_id, image_id)
            instance = hdf.create_group(key)
            if mask is not None:
                mask_array = CT.get_array(mask)
                instance.create_dataset('mask', data=mask_array)
            image_array = CT.get_array(image)
            instance.create_dataset('image', data=image_array)
            for k in image.GetMetaDataKeys():
                value = image.GetMetaData(k)
                instance['image'].attrs[k] = value


def extract_radiomics_features(catalog_file_path, config_path, CT, sep=','):
    """ Generate radiomics features.

    The radiomics features are generated using pyradiomics package.

    Args:
        catalog_file_path (str): Address of a catalog file. A Catalog file is a
            tabular file containing 4 columns. These are (1) sample_id,
            (2) image_id, (3) image_src, and (4) mask_src, respectively.
        config_path (str): Address of the file used for the configuration of
            pyradiomics.
        CT: A CT object type such as DICOMCTDIR.

    Returns:
        A dictionary, where the keys are (sample_id, image_id) and the values
            are a dictionary of features.

    """
    hand_craft = HandCraft(config_path=config_path)
    # Build the data_sequence to define the images/masks
    data_sequence = read_catalog(catalog_file_path=catalog_file_path, sep=sep)
    features = dict()
    for (sample_id, image_id, image_src, mask_src) in data_sequence:
        if mask_src == '':
            raise ValueError('mask is missing for the CT at ', image_src)
        instance = CT(sample_id, image_id, image_src, mask_src)
        image, mask = instance.load()
        hc_features = hand_craft.extract(image, mask)
        features[(sample_id, image_id)] = hc_features
    return features


def dump_radiomics_features_2_json(json_file_path, catalog_file_path,
                                   config_path, CT, sep=','):
    """ Generate and save radiomics features tp a JSON file.

    The radiomics features are generated using pyradiomics package.

    Args:
        json_file_path (str): Address of a catalog file. A Catalog file is a
            tabular file containing 4 columns. These are (1) sample_id,
            (2) image_id, (3) image_src, and (4) mask_src, respectively.
        output_file_path (str): Address of the JSON file to hold the radiomics
        features.
        config_path (str): Address of the file used for the configuration of
            pyradiomics.
        CT: A CT object type such as DICOMCTDIR.

    """
    serializeable_results = {}
    features = extract_radiomics_features(catalog_file_path, config_path, CT,
                                          sep)
    for (sample_id, image_id), hc_features in features.items():
        # JASON Serialize numpy.ndarrays
        results = json_serialize(hc_features)
        serializeable_results['{},{}'.format(sample_id, image_id)] = results
    with open(json_file_path, 'w') as fout:
        json.dump(serializeable_results, fout)


def json_serialize(features):
    """ Get json serializable dictionary from a dictionary of numpy objects.

    Numpy objects are not currently json serializable. This method generates a
    serializable version for such a dictionary.

    Args:
        features(dict): A dictionary of numpy objects.

    Returns:
        A jason serializable dictionary.
    """
    results = {}
    for k, value in features.items():
        if isinstance(value, np.ndarray):
            # Handel numpy 0-d arrays, as they are not iterable
            if value.ndim == 0:
                value = list(np.array(value, ndmin=1))[0]
            else:
                value = list(value)
        results[k] = value
    return results


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
