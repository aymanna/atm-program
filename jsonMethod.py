"""
Custom method for getting and writing json file
"""

import json
from os import path


def retrieve(filePath: str):
    """Returns a json file by converting it to a  python data."""
    if path.isfile(filePath) is False:
        raise Exception("File not found")

    with open(filePath, 'r') as f:
        data = json.load(f)

    return data


def update(obj: object, filePath: str, multiple=True, indent=4):
    """
    Updates a json file by inserting a list or a dictionary to the json file,
    with formatted.
    Also returns the end result.
    
    >>> jsonMethod.retrieve(json_0)
    [1,2,3,4]
    >>> jsonMethod.update(5,json_0)
    [1,2,3,4,5]


    >>> jsonMethod.retrieve(json_1)
    [
        {
            "Name": "Person_1",
            "Age": 11
        },
        {
            "Name": "Person_2",
            "Age": 22
        }
    ]
    >>> data = {"Name": "Person_3", "Age": 15}
    >>> jsonMethod.update(data, json_1)
    [
        {
            "Name": "Person_1",
            "Age": 11
        },
        {
            "Name": "Person_2",
            "Age": 22
        },
        {
            "Name": "Person_3",
            "Age": 15
        }
    ]


    >>> jsonMethod.retrieve(json_2)
    {
        key1: value1,
        key2: value2
    }
    >>> data = {key3: value3}
    >>> jsonMethod.update(data, json_2)
    {
        key1: value1,
        key2: value2,
        key3: value3
    }
    """

    if path.isfile(filePath) is False:
        raise Exception("File not found")

    with open(filePath, 'r') as f:
        data = json.load(f)

    if type(data) is list:

        if multiple:
            data.extend(obj)
        else:
            data.append(obj)

        with open(filePath, 'w') as f:
            json.dump(data, f, indent=indent, separators=(',', ': '))

        return data

    if type(obj) is list:
        raise Exception("A dict data can only be insert to a dict json")

    for key, value in obj.items():
        data[key] = value

    with open(filePath, 'w') as f:
        json.dump(data, f, indent=indent, separators=(',', ': '))

    return data