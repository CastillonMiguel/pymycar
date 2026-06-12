"""
Suspension files
================

This module provides functions to load and save suspension geometry data.

"""

import numpy as np

def load_defined_geometry(file_path):
    """
    Load suspension geometry data from a text file into a dictionary.

    Parameters
    ----------
    file_path : str
        The path to the text file containing the suspension geometry data.

    Returns
    -------
    dict
        A dictionary where the keys are the names of the suspension points and the values are numpy arrays containing the x, y, and z coordinates.
    """
    data = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:  # Skip the header line
            parts = line.split()
            key = parts[0]
            values = list(map(float, parts[1:]))
            data[key] = np.array(values)
    return data


def saved_defined_geometry(data, file_path):
    """
    Save suspension geometry data from a dictionary to a text file.

    Parameters
    ----------
    data : dict
        A dictionary where the keys are the names of the suspension points and the values are numpy arrays containing the x, y, and z coordinates.
    file_path : str
        The path to the text file where the suspension geometry data will be saved.
    """
    with open(file_path, 'w') as file:
        file.write("                    x       y      z\n")
        for key, values in data.items():
            # Ensure alignment and precision for x, y, and z
            file.write(f"{key:15} {values[0]:7.1f} {values[1]:7.1f} {values[2]:7.1f}\n")         
