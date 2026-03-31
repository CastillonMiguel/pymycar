"""
Functions
=========

"""

###############################################################################
# Import necessary libraries
# --------------------------
import os
import numpy as np

def generate_axis_range(position, max_increase, max_decrease, step, axis=2):
    """
    Generate a range of values along a selected axis around a reference position.

    Parameters:
    - position (numpy.ndarray): Reference position [x, y, z].
    - max_increase (float): Maximum increase from the reference value.
    - max_decrease (float): Maximum decrease from the reference value.
    - step (float): Increment step.
    - axis (int): Coordinate index (0=x, 1=y, 2=z). Default = 2.

    Returns:
    - values (numpy.ndarray): Generated axis values.
    - initial_index (int): Index of the reference value in the array.
    """

    if axis not in [0, 1, 2]:
        raise ValueError("axis must be 0 (x), 1 (y), or 2 (z)")

    base_value = position[axis]

    max_increase = abs(max_increase)
    max_decrease = abs(max_decrease)

    positive_values = np.arange(base_value, base_value + max_increase + step, step)
    negative_values = np.arange(base_value - max_decrease, base_value, step)

    values = np.concatenate([negative_values, positive_values])

    initial_index = np.where(np.isclose(values, base_value))[0][0]

    return values, initial_index