""" This file is part of CartoPluie.

 CartoPluie is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

 CartoPluie is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License along with CartoPluie. If not, see <https://www.gnu.org/licenses/>. 

 Main contributors:
 Benoit Adam, INP school (Grenoble, France)
 Cobard Laurine, INP school (Grenoble, France)
 Fine Gaetan, INP school (Grenoble, France)
 Jay-Allemand Maxime, Hydris-Hydrologie corp. (Montferrier-sur-Lez, France)

 Contact : maxime.jay.allemand@hydris-hydrologie.fr

 <The program CartoPluie begins now>"""
from __future__ import annotations

import os
import h5py
import numpy as np
import numbers
import pandas as pd
import datetime
import time

from ..src import object_handler
import gc


def close_all_fdh5_file():

    for obj in gc.get_objects():   # Browse through ALL objects
        if isinstance(obj, h5py.File):   # Just HDF5 files
            try:
                print(f"try closing {obj}")
                obj.close()
            except:
                pass  # Was already closed


def open_hdf5(path, read_only=False, replace=False, wait_time=0):
    """
    Open or create an HDF5 file.

    Parameters
    ----------
    path : str
        The file path.
    read_only : boolean
        If true the access to the hdf5 fil is in read-only mode. Multi process can read the same hdf5 file simulteneously. This is not possible when access mode are append 'a' or write 'w'.
    replace: Boolean
        If true, the existing hdf5file is erased

    Returns
    -------
    f :
        A HDF5 object.

    Examples
    --------
    >>> hdf5=smash.tools.hdf5_handler.open_hdf5("./my_hdf5.hdf5")
    >>> hdf5.keys()
    >>> hdf5.attrs.keys()
    """
    f = None
    wait = 0
    while wait <= wait_time:

        f = None
        exist_file=True
        
        try:

            if read_only:
                if os.path.isfile(path):
                    f = h5py.File(path, "r")

                else:
                    exist_file=False
                    raise ValueError(f"File {path} does not exist.")

            else:
                if replace:
                    f = h5py.File(path, "w")

                else:
                    if os.path.isfile(path):
                        f = h5py.File(path, "a")

                    else:
                        f = h5py.File(path, "w")
        except:
            pass

        if f is None:
            if not exist_file:
                print(f"File {path} does not exist.")
                return f
            else:
                print(
                    f"The file {path} is unvailable, waiting {wait}/{wait_time}s")

            wait = wait + 1

            if wait_time > 0:
                time.sleep(1)

        else:
            break

    return f


def add_hdf5_sub_group(hdf5, subgroup=None):
    """
    Create a new subgroup in a HDF5 object

    Parameters
    ----------
    hdf5 : object
        An hdf5 object opened with open_hdf5()
    subgroup: str
        Path to a subgroub that must be created

    Returns
    -------
    hdf5 :
        the HDF5 object.

    Examples
    --------
    >>> hdf5=smash.tools.hdf5_handler.open_hdf5("./model_subgroup.hdf5", replace=True)
    >>> hdf5=smash.tools.hdf5_handler.add_hdf5_sub_group(hdf5, subgroup="mygroup")
    >>> hdf5.keys()
    >>> hdf5.attrs.keys()
    """
    if subgroup is not None:
        if subgroup == "":
            subgroup = "./"

        hdf5.require_group(subgroup)

    return hdf5


def _dump_object_to_hdf5_from_list_attribute(hdf5, instance, list_attr):
    """
    dump a object to a hdf5 file from a list of attributes

    Parameters
    ----------
    hdf5 : object
        an hdf5 object
    instance : object
        a custom python object.
    list_attr : list
        a list of attribute
    """
    if isinstance(list_attr, list):
        for attr in list_attr:
            if isinstance(attr, str):
                _dump_object_to_hdf5_from_str_attribute(hdf5, instance, attr)

            elif isinstance(attr, list):
                _dump_object_to_hdf5_from_list_attribute(hdf5, instance, attr)

            elif isinstance(attr, dict):
                _dump_object_to_hdf5_from_dict_attribute(hdf5, instance, attr)

            else:
                raise ValueError(
                    f"inconsistent {attr} in {list_attr}. {attr} must be a an instance of dict, list or str"
                )

    else:
        raise ValueError(f"{list_attr} must be a instance of list.")


def _dump_object_to_hdf5_from_dict_attribute(hdf5, instance, dict_attr):
    """
    dump a object to a hdf5 file from a dictionary of attributes

    Parameters
    ----------
    hdf5 : object
        an hdf5 object
    instance : object
        a custom python object.
    dict_attr : dict
        a dictionary of attribute
    """
    if isinstance(dict_attr, dict):
        for attr, value in dict_attr.items():
            hdf5 = add_hdf5_sub_group(hdf5, subgroup=attr)

            try:
                sub_instance = getattr(instance, attr)

            except:
                sub_instance = instance

            if isinstance(value, dict):
                _dump_object_to_hdf5_from_dict_attribute(
                    hdf5[attr], sub_instance, value
                )

            if isinstance(value, list):
                _dump_object_to_hdf5_from_list_attribute(
                    hdf5[attr], sub_instance, value
                )

            elif isinstance(value, str):
                _dump_object_to_hdf5_from_str_attribute(
                    hdf5[attr], sub_instance, value)

            else:
                raise ValueError(
                    f"inconsistent '{attr}' in '{dict_attr}'. Dict({attr}) must be a instance of dict, list or str"
                )

    else:
        raise ValueError(f"{dict_attr} must be a instance of dict.")


def _dump_object_to_hdf5_from_str_attribute(hdf5, instance, str_attr):
    """
    dump a object to a hdf5 file from a string attribute

    Parameters
    ----------
    hdf5 : object
        an hdf5 object
    instance : object
        a custom python object.
    str_attr : str
        a string attribute
    """
    if isinstance(str_attr, str):
        try:
            value = getattr(instance, str_attr)

            if isinstance(value, (np.ndarray, list)):

                # TODO: do the same than _dump_dict_to_hdf5

                if isinstance(value, list):
                    value = np.array(value)

                if value.dtype == "object" or value.dtype.char == "U":
                    value = value.astype("S")

                # data_type=value.dtype
                # if value.dtype == "object" or value.dtype.char == "U":
                #      #value = value.astype("b")
                #      value = value.astype("O")
                #      data_type = h5py.string_dtype(encoding='utf-8')

                # remove dataset if exist
                if str_attr in hdf5.keys():
                    del hdf5[str_attr]

                hdf5.create_dataset(
                    str_attr,
                    shape=value.shape,
                    dtype=value.dtype,
                    data=value,
                    compression="gzip",
                    chunks=True,
                )

            elif value is None:
                hdf5.attrs[str_attr] = "_None_"

            elif isinstance(value, str):
                hdf5.attrs[str_attr] = value.encode()

            else:
                hdf5.attrs[str_attr] = value

        except:
            raise ValueError(
                f"Unable to dump attribute {str_attr} with value {value} from {instance}"
            )

    else:
        raise ValueError(f"{str_attr} must be a instance of str.")


def _dump_object_to_hdf5_from_iteratable(hdf5, instance, iteratable=None):
    """
    dump a object to a hdf5 file from a iteratable object list or dict

    Parameters
    ----------
    hdf5 : object
        an hdf5 object
    instance : object
        a custom python object.
    iteratable : list | dict
        a list or a dict of attribute

    Examples
    --------
    setup, mesh = smash.load_dataset("cance")
    model = smash.Model(setup, mesh)
    model.run(inplace=True)

    hdf5=smash.tools.hdf5_handler.open_hdf5("./model.hdf5", replace=True)
    hdf5=smash.tools.hdf5_handler.add_hdf5_sub_group(hdf5, subgroup="model1")
    keys_data=smash.io.hdf5_io.generate_smash_object_structure(model,typeofstructure="medium")
    smash.tools.hdf5_handler._dump_object_to_hdf5_from_iteratable(hdf5["model1"], model, keys_data)

    hdf5=smash.tools.hdf5_handler.open_hdf5("./model.hdf5", replace=False)
    hdf5=smash.tools.hdf5_handler.add_hdf5_sub_group(hdf5, subgroup="model2")
    keys_data=smash.io.hdf5_io.generate_smash_object_structure(model,typeofstructure="light")
    smash.tools.hdf5_handler._dump_object_to_hdf5_from_iteratable(hdf5["model2"], model, keys_data)
    """
    if isinstance(iteratable, list):
        _dump_object_to_hdf5_from_list_attribute(hdf5, instance, iteratable)

    elif isinstance(iteratable, dict):
        _dump_object_to_hdf5_from_dict_attribute(hdf5, instance, iteratable)

    else:
        raise ValueError(f"{iteratable} must be a instance of list or dict.")


def _dump_dict_to_hdf5(hdf5, dictionary):
    """
    dump a dictionary to an hdf5 file

    Parameters
    ----------
    hdf5 : object
        an hdf5 object
    dictionary : dict
        a custom python dictionary
    """
    if isinstance(dictionary, dict):
        for attr, value in dictionary.items():
            # print("looping:",attr,value)
            try:

                attribute_name = str(attr)
                for character in '/ ':
                    attribute_name = attribute_name.replace(
                        character, '_')

                if isinstance(value, dict):
                    # print("---> dictionary: ",attr, value)

                    hdf5 = add_hdf5_sub_group(hdf5, subgroup=attribute_name)
                    _dump_dict_to_hdf5(hdf5[attribute_name], value)

                else:

                    # support special case:
                    if hasattr(value, 'dtype'):
                        # datetime64 are not supported => switch to string
                        if value.dtype.char == "M":
                            ListDate = value.tolist()
                            ListDateStr = list()

                            for date in ListDate:
                                ListDateStr.append(
                                    date.strftime("%Y-%m-%dT%H:%M"))

                            value = np.array(ListDateStr)
                            value = value.astype("O")
                            data_type = h5py.string_dtype(encoding='utf-8')

                    if isinstance(value, (np.ndarray, list)):
                        # print("---> (np.ndarray, list): ",attr, value)

                        if isinstance(value, list):
                            value = np.array(value)

                        # if isinstance(value, np.ndarray):
                        if len(value.dtype) > 0 and len(value.dtype.names) > 0:

                            hdf5 = add_hdf5_sub_group(
                                hdf5, subgroup=attribute_name)
                            _dump_ndarray_to_hdf5(hdf5[attribute_name], value)

                        else:

                            data_type = value.dtype

                            if value.dtype == "object" or value.dtype.char == "U":

                                value = value.astype("O")
                                data_type = h5py.string_dtype(encoding='utf-8')

                            # remove dataset if exist
                            if attribute_name in hdf5.keys():
                                del hdf5[attribute_name]

                            hdf5.create_dataset(
                                attribute_name,
                                shape=value.shape,
                                dtype=data_type,
                                data=value,
                                compression="gzip",
                                chunks=True,
                            )

                    elif value is None:
                        hdf5.attrs[attr] = "_None_"

                    elif isinstance(value, str):
                        hdf5.attrs[str(attr)] = value.encode()

                    elif isinstance(value, numbers.Number):

                        hdf5.attrs[str(attr)] = value

                    elif isinstance(value, (pd.Timestamp, np.datetime64, datetime.date)):

                        hdf5.attrs[str(attr)] = str(value)

                    else:

                        if attribute_name in hdf5.keys():
                            del hdf5[attribute_name]

                        hdf5 = add_hdf5_sub_group(
                            hdf5, subgroup=attribute_name)

                        newdict = object_handler.read_object_as_dict(value)

                        _dump_dict_to_hdf5(hdf5[attribute_name], newdict)
            except:

                raise ValueError(
                    f"Unable to save attribute {str(attr)} with value {value}")

    else:

        raise ValueError(f"{dictionary} must be a instance of dict.")


# TODO recreate the ndarray with indexes and dtype when reading the hdf5...
def _dump_ndarray_to_hdf5(hdf5, value):
    """
    dump a ndarray data structure to an hdf5 file: this functions create a group ndarray_ds and store each component of the ndarray as a dataset. Plus it add 2 datasets which store the dtypes (ndarray_dtype) and labels (ndarray_indexes).

    Parameters
    ----------
    hdf5 : object
        an hdf5 object
    value : ndarray
        an ndarray data structure with different datatype
    """
    # save ndarray datastructure

    hdf5 = add_hdf5_sub_group(hdf5, subgroup="ndarray_ds")
    hdf5_data = hdf5["ndarray_ds"]

    for item in value.dtype.names:

        ndarray_value = value[item]
        data_type = ndarray_value.dtype

        if ndarray_value.dtype.char == "O" or ndarray_value.dtype == "object" or ndarray_value.dtype.char == "U":
            # value = value.astype("b")
            # first force convert to U is object, then convert to O
            ndarray_value = value[item].astype("U")
            ndarray_value = ndarray_value.astype("O")
            data_type = h5py.string_dtype(encoding='utf-8')

        # datetime64 are not supported => switch to string
        if ndarray_value.dtype.char == "M":
            ListDate = value[item].tolist()
            ListDateStr = list()

            for date in ListDate:
                ListDateStr.append(date.strftime("%Y-%m-%dT%H:%M"))

            ndarray_value = np.array(ListDateStr)
            ndarray_value = ndarray_value.astype("O")
            data_type = h5py.string_dtype(encoding='utf-8')

        attribute_name = item
        for character in '/ ':
            attribute_name = attribute_name.replace(character, '_')

        # remove dataset if exist
        if attribute_name in hdf5_data.keys():
            del hdf5_data[attribute_name]

        # print(attribute_name,data_type,ndarray_value)

        hdf5_data.create_dataset(
            attribute_name,
            shape=ndarray_value.shape,
            dtype=data_type,
            data=ndarray_value,
            compression="gzip",
            chunks=True,
        )

    index = np.array(value.dtype.descr)[:, 0]
    dtype = np.array(value.dtype.descr)[:, 1]
    index = index.astype("O")
    dtype = dtype.astype("O")
    data_type = h5py.string_dtype(encoding='utf-8')

    if "ndarray_dtype" in hdf5_data.keys():
        del hdf5_data["ndarray_dtype"]

    hdf5_data.create_dataset(
        "ndarray_dtype",
        shape=dtype.shape,
        dtype=data_type,
        data=dtype,
        compression="gzip",
        chunks=True,
    )

    if "ndarray_indexes" in hdf5_data.keys():
        del hdf5_data["ndarray_indexes"]

    hdf5_data.create_dataset(
        "ndarray_indexes",
        shape=index.shape,
        dtype=data_type,
        data=index,
        compression="gzip",
        chunks=True,
    )


def _read_ndarray_datastructure(hdf5):
    """
    read a ndarray data structure from hdf5 file

    Parameters
    ----------
    hdf5 : object
        an hdf5 object at the roots of the ndarray datastructure

    Return
    ----------
    ndarray : the ndarray
    """

    if 'ndarray_ds' in list(hdf5.keys()):

        decoded_item = list()
        for it in hdf5['ndarray_ds/ndarray_dtype'][:]:
            decoded_item.append(it.decode())
        list_dtypes = decoded_item

        decoded_item = list()
        for it in hdf5['ndarray_ds/ndarray_indexes'][:]:
            decoded_item.append(it.decode())
        list_indexes = decoded_item

        len_data = len(hdf5[f'ndarray_ds/{list_indexes[0]}'][:])

        list_datatype = list()
        for i in range(len(list_indexes)):
            list_datatype.append((list_indexes[i], list_dtypes[i]))

        datatype = np.dtype(list_datatype)

        ndarray = np.zeros(len_data, dtype=datatype)

        for i in range(len(list_indexes)):

            data = hdf5[f'ndarray_ds/{list_indexes[i]}'][:]

            # hack for datetime: suppose dtype='|M.. or <M..'
            if list_dtypes[i][1] == "M":

                list_datetime = list()
                for date in data.tolist():
                    list_datetime.append(np.datetime64(date))

                data = np.array(list_datetime)
                data = data[:].astype(list_dtypes[i])

            else:

                data = data[:].astype(list_dtypes[i])

            if data[:].dtype.char == "S":

                values = data[:].astype("U")

            elif data[:].dtype.char == "O":

                # decode list if required
                decoded_item = list()
                for it in data[:]:
                    decoded_item.append(it.decode())

                values = decoded_item

            else:
                values = data[:]

            ndarray[list_indexes[i]] = values

        return ndarray


def save_dict_to_hdf5(path_to_hdf5, dictionary=None, location="./", replace=False, wait_time=0):
    """
    dump a dictionary to an hdf5 file

    Parameters
    ----------
    path_to_hdf5 : str
        path to the hdf5 file
    dictionary : dict | None
        a dictionary containing the data to be saved
    location : str
        path location or subgroup where to write data in the hdf5 file
    replace : Boolean
        replace an existing hdf5 file. Default is False

    Examples
    --------
    setup, mesh = smash.load_dataset("cance")
    model = smash.Model(setup, mesh)
    model.run(inplace=True)

    smash.tools.hdf5_handler.save_dict_to_hdf5("saved_dictionary.hdf5",mesh)
    """
    if isinstance(dictionary, dict):
        hdf5 = open_hdf5(path_to_hdf5, replace=replace, wait_time=wait_time)

        if hdf5 is None:
            return

        hdf5 = add_hdf5_sub_group(hdf5, subgroup=location)
        _dump_dict_to_hdf5(hdf5[location], dictionary)

    else:
        raise ValueError(f"The input {dictionary} must be a instance of dict.")

    hdf5.close()


def save_object_to_hdf5(
    f_hdf5, instance, keys_data=None, location="./", sub_data=None, replace=False, wait_time=0
):
    """
    dump an object to an hdf5 file

    Parameters
    ----------
    f_hdf5 : str
        path to the hdf5 file
    instance : object
        A custom python object to be saved into an hdf5
    keys_data : list | dict
        optional, a list or a dictionary of the attribute to be saved
    location : str
        path location or subgroup where to write data in the hdf5 file
    sub_data : dict | None
        optional, a extra dictionary containing extra-data to be saved along the object
    replace : Boolean
        replace an existing hdf5 file. Default is False
    """

    if keys_data is None:
        keys_data = object_handler.generate_object_structure(instance)

    # print(keys_data)

    hdf5 = open_hdf5(f_hdf5, replace=replace, wait_time=wait_time)

    if hdf5 is None:
        return None

    hdf5 = add_hdf5_sub_group(hdf5, subgroup=location)

    _dump_object_to_hdf5_from_iteratable(hdf5[location], instance, keys_data)

    if isinstance(sub_data, dict):
        _dump_dict_to_hdf5(hdf5[location], sub_data)

    hdf5.close()


def read_hdf5file_as_dict(path_to_hdf5, location="./", wait_time=0):
    """
    Open, read and close an hdf5 file

    Parameters
    ----------
    path_to_hdf5 : str
        path to the hdf5 file
    location: str
        place in the hdf5 from which we start reading the file

    Return
    --------
    dictionary : dict, a dictionary of all keys and attribute included in the hdf5 file

    Examples
    --------
    #read an hdf5 file
    dictionary=hdf5_handler.read_hdf5file_as_dict(hdf5["model1"])
    """

    hdf5 = open_hdf5(path_to_hdf5, read_only=True, wait_time=wait_time)

    if hdf5 is None:
        return None

    dictionary = read_hdf5_as_dict(hdf5[location])

    hdf5.close()

    return dictionary


def read_hdf5_as_dict(hdf5):
    """
    Load an hdf5 file

    Parameters
    ----------
    hdf5 : str
        an instance of hdf5, open with the function open_hdf5()

    Return
    --------
    dictionary : dict, a dictionary of all keys and attribute included in the hdf5 file

    Examples
    --------
    #read only a part of an hdf5 file
    hdf5=hdf5_handler.open_hdf5("./multi_model.hdf5")
    dictionary=hdf5_handler.read_hdf5_as_dict(hdf5["model1"])
    dictionary.keys()
    """

    if not isinstance(hdf5, (h5py.File, h5py.Group, h5py.Dataset, h5py.Datatype)):
        print('Error: input arg is not an instance of hdf5.File()')
        return {}

    dictionary = {}

    for key, item in hdf5.items():

        if str(type(item)).find("group") != -1:

            if key == 'ndarray_ds':

                # dictionary.update({key: _read_ndarray_datastructure(hdf5)})
                return _read_ndarray_datastructure(hdf5)

            else:

                dictionary.update({key: read_hdf5_as_dict(item)})

            list_attr = list(item.attrs.keys())

            for key_attr in list_attr:
                # check if value is equal to "_None_" (None string because hdf5 does not supported)
                if isinstance(item.attrs[key_attr], str) and item.attrs[key_attr] == "_None_":
                    dictionary[key].update({key_attr: None})
                elif isinstance(item.attrs[key_attr], bytes):
                    dictionary[key].update(
                        {key_attr: item.attrs[key_attr].decode()})
                else:
                    dictionary[key].update({key_attr: item.attrs[key_attr]})

        if str(type(item)).find("dataset") != -1:

            if item[:].dtype.char == "S":

                values = item[:].astype("U")

            elif item[:].dtype.char == "O":

                # decode list if required
                decoded_item = list()
                for it in item[:]:
                    decoded_item.append(it.decode())

                values = decoded_item

            else:
                values = item[:]

            dictionary.update({key: values})

            list_attr = list(item.attrs.keys())

            for key_attr in list_attr:
                # check if value is equal to "_None_" (None string because hdf5 does not supported)
                if isinstance(item.attrs[key_attr], str) and item.attrs[key_attr] == "_None_":
                    dictionary.update({key_attr: None})
                elif isinstance(item.attrs[key_attr], bytes):
                    dictionary.update(
                        {key_attr: item.attrs[key_attr].decode()})
                else:
                    dictionary.update({key_attr: item.attrs[key_attr]})

    list_attr = list(hdf5.attrs.keys())

    for key_attr in list_attr:
        # check if value is equal to "_None_" (None string because hdf5 does not supported)
        if isinstance(hdf5.attrs[key_attr], str) and hdf5.attrs[key_attr] == "_None_":
            dictionary.update({key_attr: None})
        elif isinstance(hdf5.attrs[key_attr], bytes):
            dictionary.update({key_attr: hdf5.attrs[key_attr].decode()})
        else:
            dictionary.update({key_attr: hdf5.attrs[key_attr]})

    return dictionary


def get_hdf5_attribute(path_to_hdf5=str(), location="./", attribute=None, wait_time=0):
    """
    Get the value of an attribute in the hdf5file

    Parameters
    ----------
    path_to_hdf5 : str
        the path to the hdf5file
    location : str
        path inside the hdf5 where the attribute is stored
    attribute: str
        attribute name

    Return
    --------
    return_attribute : the value of the attribute

    Examples
    --------
    #rget an attribute
    attribute=hdf5_handler.get_hdf5_attribute("./multi_model.hdf5",attribute=my_attribute_name)
    """

    hdf5_base = open_hdf5(path_to_hdf5, read_only=True, wait_time=wait_time)

    if hdf5_base is None:
        return None

    hdf5 = hdf5_base[location]

    return_attribute = hdf5.attrs[attribute]

    hdf5_base.close()

    return return_attribute


def get_hdf5_dataset(path_to_hdf5=str(), location="./", dataset=None, wait_time=0):
    """
    Get the value of an attribute in the hdf5file

    Parameters
    ----------
    path_to_hdf5 : str
        the path to the hdf5file
    location : str
        path inside the hdf5 where the attribute is stored
    dataset: str
        dataset name

    Return
    --------
    return_dataset : the value of the attribute

    Examples
    --------
    #get a dataset
    dataset=hdf5_handler.get_hdf5_dataset("./multi_model.hdf5",dataset=my_dataset_name)
    """

    hdf5_base = open_hdf5(path_to_hdf5, read_only=True, wait_time=wait_time)

    if hdf5_base is None:
        return None

    hdf5 = hdf5_base[location]

    return_dataset = hdf5[dataset][:]

    hdf5_base.close()

    return return_dataset


def get_hdf5file_item(path_to_hdf5=str(), location="./", item=None, wait_time=0):
    """
    Get a custom item in an hdf5file

    Parameters
    ----------
    path_to_hdf5 : str
        the path to the hdf5file
    location : str
        path inside the hdf5 where the attribute is stored. If item is None, item is set to basename(location)
    item: str
        item name

    Return
    --------
    return : custom value. can be an hdf5 object (group), an numpy array, a string, a float, an int ...

    Examples
    --------
    #get the dataset 'dataset'
    dataset=hdf5_handler.get_hdf5_item("./multi_model.hdf5",location="path/in/hdf5/dataset")
    """

    hdf5 = open_hdf5(path_to_hdf5, read_only=True, wait_time=wait_time)

    if hdf5 is None:
        return None

    hdf5_item = get_hdf5_item(hdf5_instance=hdf5, location=location, item=item)

    hdf5.close()

    return hdf5_item


def get_hdf5_item(hdf5_instance=None, location="./", item=None):
    """
    Get a custom item in an hdf5file

    Parameters

    hdf5_instance : hdf5 instance
        an instance of an hdf5
    location : str
        path inside the hdf5 where the attribute is stored. If item is None, item is set to basename(location)
    item: str
        item name

    Return
    --------
    return : custom value. can be an hdf5 object (group), an numpy array, a string, a float, an int ...

    Examples
    --------
    #get the dataset 'dataset'
    dataset=hdf5_handler.get_hdf5_item("./multi_model.hdf5",location="path/in/hdf5/dataset")
    """

    if item is None and isinstance(location, str):
        head, tail = os.path.split(location)
        if len(tail) > 0:
            item = tail
        location = head

    if not isinstance(item, str):
        print(f"Bad search item:{item}")
        return None

        return None

    # print(f"Getting item '{item}' at location '{location}'")
    hdf5 = hdf5_instance[location]

    # first search in the attribute
    list_attribute = hdf5.attrs.keys()
    if item in list_attribute:
        return hdf5.attrs[item]

    # then search in groups and dataset
    list_keys = hdf5.keys()
    if item in list_keys:

        hdf5_item = hdf5[item]

        # print("Got Item ", hdf5_item)

        if str(type(hdf5_item)).find("group") != -1:

            returned_dict = read_hdf5_as_dict(hdf5_item)
            return returned_dict

        elif str(type(hdf5_item)).find("dataset") != -1:

            if hdf5_item[:].dtype.char == "S":

                values = hdf5_item[:].astype("U")

            elif hdf5_item[:].dtype.char == "O":

                # decode list if required
                decoded_item = list()
                for it in hdf5_item[:]:
                    decoded_item.append(it.decode())

                values = decoded_item

            else:

                values = hdf5_item[:]

            return values

        else:

            return hdf5_item

    else:

        return None


def search_in_hdf5file(path_to_hdf5, key=None, location="./", wait_time=0):
    """
    Search key in an hdf5 and return a list of [locations, datatype, key name, values]. Value and key are returned only if the key is an attribute or a dataset (None otherwise)

    Parameters
    ----------
    path_to_hdf5 : str
        the path to the hdf5file
    key: str
        key to search in the hdf5file
    location : str
        path inside the hdf5 where to start the research

    Return
    --------
    return_dataset : the value of the attribute

    Examples
    --------
    #search in a hdf5file
    matchkey=hdf5_handler.search_in_hdf5file(hdf5filename, key='Nom_du_BV',location="./")
    """
    if key is None:
        print("Nothing to search, use key=")
        return []

    hdf5 = open_hdf5(path_to_hdf5, read_only=True, wait_time=wait_time)

    if hdf5 is None:
        return None

    results = search_in_hdf5(hdf5, key, location=location)

    hdf5.close()

    return results


def search_in_hdf5(hdf5_base, key=None, location="./"):
    """
    Search key in an hdf5 and return a list of [locations, datatype, key name, values]. Value and key are returned only if the key is an attribute or a dataset (None otherwise)

    Parameters
    ----------
    hdf5_base : instance of hdf5
        opened instance of the hdf5
    key: str
        key to search in the hdf5file
    location : str
        path inside the hdf5 where to start the research

    Return
    --------
    return_dataset : the value of the attribute

    Examples
    --------
    #search in a hdf5
    hdf5=hdf5_handler.open_hdf5(hdf5_file)
    matchkey=hdf5_handler.search_in_hdf5(hdf5, key='Nom_du_BV',location="./")
    hdf5.close()
    """
    if key is None:
        print("Nothing to search, use key=")
        return []

    result = []

    hdf5 = hdf5_base[location]

    list_attribute = hdf5.attrs.keys()

    if key in list_attribute:
        result.append({"path": location, "key": key,
                      "datatype": "attribute", "value": hdf5.attrs[key]})

    for hdf5_key, item in hdf5.items():

        if str(type(item)).find("group") != -1:

            sub_location = os.path.join(location, hdf5_key)

            if hdf5_key == key:
                result.append({"path": sub_location, "key": None,
                              "datatype": "group", "value": None})

            res = search_in_hdf5(hdf5_base, key, sub_location)

            if len(res) > 0:
                result.append(res[0])

        if str(type(item)).find("dataset") != -1:

            if hdf5_key == key:

                if item[:].dtype.char == "S":

                    values = item[:].astype("U")

                elif item[:].dtype.char == "O":

                    # decode list if required
                    decoded_item = list()
                    for it in item[:]:
                        decoded_item.append(it.decode())

                    values = decoded_item

                else:

                    values = item[:]

                result.append({"path": location, "key": key,
                              "datatype": "dataset", "value": values})

    return result


def hdf5file_view(path_to_hdf5, location="./", max_depth=None, level_base='>', level_sep="--", depth=None, wait_time=0):
    """
    Search key in an hdf5 and return a list of [locations, datatype, key name, values]. Value and key are returned only if the key is an attribute or a dataset (None otherwise)

    Parameters
    ----------
    path_to_hdf5 : str
        the path to the hdf5file
    key: str
        key to search in the hdf5file
    location : str
        path inside the hdf5 where to start the research

    Return
    --------
    return_dataset : the value of the attribute

    Examples
    --------
    #search in a hdf5file
    matchkey=hdf5_handler.search_in_hdf5file(hdf5filename, key='Nom_du_BV',location="./")
    """

    hdf5 = open_hdf5(path_to_hdf5, read_only=True, wait_time=wait_time)

    if hdf5 is None:
        return None

    results = hdf5_view(hdf5, location=location, max_depth=max_depth,
                        level_base=level_base, level_sep=level_sep, depth=depth)

    hdf5.close()

    return results


def hdf5_view(hdf5_base, location="./", max_depth=None, level_base='>', level_sep="--", depth=None):
    """
    Search key in an hdf5 and return a list of [locations, datatype, key name, values]. Value and key are returned only if the key is an attribute or a dataset (None otherwise)

    Parameters
    ----------
    hdf5_base : instance of hdf5
        opened instance of the hdf5
    key: str
        key to search in the hdf5file
    location : str
        path inside the hdf5 where to start the research

    Return
    --------
    return_dataset : the value of the attribute

    Examples
    --------
    #search in a hdf5
    hdf5=hdf5_handler.open_hdf5(hdf5_file)
    matchkey=hdf5_handler.search_in_hdf5(hdf5, key='Nom_du_BV',location="./")
    hdf5.close()
    """

    result = []

    if max_depth is not None:

        if depth is not None:
            depth = depth+1
        else:
            depth = 0

        if depth > max_depth:
            return result

    hdf5 = hdf5_base[location]

    list_attribute = hdf5.attrs.keys()

    for key in list_attribute:
        values = hdf5.attrs[key]
        sub_location = os.path.join(location, key)
        if isinstance(values, (int, float, np.int64, np.float64, np.int32, np.float32, np.bool)):
            result.append(
                f"{level_base}| {sub_location}, attribute, type={type(hdf5.attrs[key])},value={values}")
        elif isinstance(values, (str)) and len(values) < 20:
            result.append(
                f"{level_base}| {sub_location}, attribute, type={type(hdf5.attrs[key])},len={len(values)},value={values}")
        else:
            result.append(
                f"{level_base}| {sub_location}, attribute, type={type(hdf5.attrs[key])},len={len(values)}")

        print(result[-1])

    for hdf5_key, item in hdf5.items():

        if str(type(item)).find("group") != -1:

            sub_location = os.path.join(location, hdf5_key)

            # result.append({"path":sub_location, "key":None, "datatype":"group","value":None})
            result.append(f"{level_base}| {sub_location}, group")
            print(result[-1])

            res = hdf5_view(hdf5_base, sub_location, max_depth=max_depth,
                            level_base=level_base+level_sep, depth=depth)

            # if len(res)>0:
            for key, item in enumerate(res):
                result.append(item)

        if str(type(item)).find("dataset") != -1:

            if item[:].dtype.char == "S":
                values = item[:].astype("U")
            else:
                values = item[:]

            sub_location = os.path.join(location, hdf5_key)
            # result.append({"path":location, "key":key, "datatype":"dataset","value":values})
            result.append(
                f"{level_base}| {sub_location}, dataset, type={type(values)},shape={values.shape}")
            print(result[-1])

    return result
