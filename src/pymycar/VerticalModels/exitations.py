"""
Exitation
=========

This module provides functions to generate excitation signals, commonly used in 
simulations. These functions include sinusoidal signals,
both in their full form and selectively capturing only positive or negative parts, 
as well as other custom excitation signals.

"""

import numpy as np

def from_data(t, defined_time, defined_sol):
    """
    Interpolate an excitation signal from defined data points.

    Parameters
    ----------
    t : array_like
        Time values for which the signal is to be interpolated.
    defined_time : array_like
        Time values where the signal is defined.
    defined_sol : array_like
        Signal values corresponding to `defined_time`.

    Returns
    -------
    array_like
        Interpolated signal at the given time values.

    Examples
    --------
    >>> defined_time = [0, 1, 2, 3]
    >>> defined_sol = [0, 10, 5, 0]
    >>> t = np.linspace(0, 3, 100)
    >>> signal = from_data(t, defined_time, defined_sol)
    """
    return np.interp(t, defined_time, defined_sol)


def sin_exitation(t, amplitude, frequency):
    """
    Generate a sinusoidal excitation signal.

    Parameters
    ----------
    t : array_like
        Time values.
    amplitude : float
        Amplitude of the sinusoidal signal.
    frequency : float
        Frequency of the sinusoidal signal.

    Returns
    -------
    array_like
        Sinusoidal excitation signal.

    Examples
    --------
    >>> t = np.linspace(0, 10, 1000)
    >>> signal = sin_exitation(t, 1, 0.2)
    """
    w = 2 * np.pi * frequency
    return amplitude * np.sin(w * t)


def sin_possitive_part_exitation(t, amplitude, frequency):
    """
    Generate a sinusoidal excitation signal with only the positive part.

    Parameters
    ----------
    t : array_like
        Time values.
    amplitude : float
        Amplitude of the sinusoidal signal.
    frequency : float
        Frequency of the sinusoidal signal.

    Returns
    -------
    array_like
        Sinusoidal excitation signal with positive values only.

    Examples
    --------
    >>> t = np.linspace(0, 10, 1000)
    >>> signal = sin_possitive_part_exitation(t, 0.1, 0.2)
    """
    w = 2 * np.pi * frequency
    return np.maximum(amplitude * np.sin(w * t), 0)


def sin_negative_part_exitation(t, amplitude, frequency):
    """
    Generate a sinusoidal excitation signal with only the negative part.

    Parameters
    ----------
    t : array_like
        Time values.
    amplitude : float
        Amplitude of the sinusoidal signal.
    frequency : float
        Frequency of the sinusoidal signal.

    Returns
    -------
    array_like
        Sinusoidal excitation signal with negative values only.

    Examples
    --------
    >>> t = np.linspace(0, 10, 1000)
    >>> signal = sin_negative_part_exitation(t, -0.1, 0.2)
    """
    w = 2 * np.pi * frequency
    return np.minimum(amplitude * np.sin(w * t), 0)


def bump_exitation(t, amplitude, frequency):
    """
    Generate a bump excitation signal.

    The bump signal is a sinusoidal signal that is active only for a fraction 
    of its period (up to half of the period).

    Parameters
    ----------
    t : array_like
        Time values.
    amplitude : float
        Amplitude of the bump signal.
    frequency : float
        Frequency of the bump signal.

    Returns
    -------
    array_like
        Bump excitation signal.

    Examples
    --------
    >>> t = np.linspace(0, 2, 1000)
    >>> signal = bump_exitation(t, 1, 1)
    """
    w = 2 * np.pi * frequency
    T = 1 / frequency
    return np.where(t <= 0.5 * T, amplitude * np.sin(w * t), 0)
