"""
Logger/library versions
=======================

This functions provides utility functions for logging simulation information and system details using Python's logging module.
It also logs versions of important libraries such as scipy, pyvista, numpy, and logging, along with system
information like platform details and Python version.

"""

import pymycar
import logging
import os
import sys
import numpy
import scipy
import time
import platform
from tabulate import tabulate

def set_logger(result_folder_name):
    """
    Set up a logger for logging simulation information.

    Parameters
    ----------
    result_folder_name : str
        The name of the folder where the log file will be stored.

    Returns
    -------
    logging.Logger
        The logger object set up for logging simulation information.

    Notes
    -----
    This function sets up a logger named 'simulation_logger' with INFO level logging.
    It creates a log file named 'simulation.log' in the specified result folder.

    Examples
    --------
    >>> logger = set_logger('results_folder')
    """
    logger = logging.getLogger('simulation_logger')
    logger.setLevel(logging.INFO)
    simulation_file_handler = logging.FileHandler(
        os.path.join(result_folder_name, 'simulation.log'))
    simulation_formatter = logging.Formatter('%(message)s')
    simulation_file_handler.setFormatter(simulation_formatter)
    logger.addHandler(simulation_file_handler)
    return logger


def log_library_versions(logger):
    """
    Log versions of important libraries.

    Parameters
    ----------
    logger : logging.Logger
        The logger object to log the information.

    Returns
    -------
    None

    Notes
    -----
    This function logs the versions of important libraries including Python, DolfinX,
    ufl, basix, numpy, and logging.
    """
    logger.info(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
    logger.info("=========== Library Versions ===========")
    logger.info(f"pymycar : {pymycar.__version__}")
    logger.info(f"numpy : {numpy.__version__}")
    logger.info(f"scipy : {scipy.__version__}")
    logger.info(f"logging : {logging.__version__}")
    logger.info("=======================================")


def log_system_info(logger):
    """
    Log system information using the provided logger.

    Parameters
    ----------
    logger : logging.Logger
        The logger object to be used for logging system information.

    Returns
    -------
    None

    Notes
    -----
    This function logs various system information including operating system,
    architecture, user name, processor, machine type, and Python version.
    """
    logger.info("=========== Platform ==================")
    logger.info(f"Operating System Information: {platform.platform()}")
    logger.info(f"Architecture : {platform.architecture()}")
    logger.info(f"User name : {platform.uname()}")
    logger.info(f"processor : {platform.processor()}")
    logger.info(f"Machine type : {platform.machine()}")
    logger.info(f"Python version : {platform.python_version()}")
    logger.info("=======================================")


def log_end_analysis(logger, totaltime=0.0):
    """
    Logs the end of an analysis process, including total simulation time and completion timestamp.

    Parameters
    ----------
    logger : logging.Logger
        The logger instance used to record the log messages.
    totaltime : float, optional
        The total simulation time to be logged. Default is 0.0.

    Notes
    -----
    This function logs several informational messages indicating the end of computations,
    the total simulation time, and the timestamp when the analysis finished.
    """
    logger.info(f"\n\n\n ====================================================")
    logger.info(f"\n\n End of computations")
    logger.info(f" Analysis finished correctly.")
    logger.info(f" total simulation time: {totaltime}")
    logger.info(f"Analysis finished on {time.strftime(
        '%a %b %d %H:%M:%S %Y', time.localtime())}")


def log_geometry_data(logger, data):
    """
    Logs 3D geometry data in a formatted table using the provided logger.
    Parameters
    ----------
    logger : logging.Logger
        The logger instance used to output the formatted table.
    data : dict
        A dictionary where each key is a component name (str) and each value is an iterable of three floats
        representing the x, y, and z coordinates of the component.
    Notes
    -----
    The geometry data is displayed in a table with columns: 'Component', 'x', 'y', and 'z'.
    Coordinates are formatted to two decimal places.
    """
    # Prepare data for tabulation
    headers = ["Component", "x", "y", "z"]
    rows = [[key, *map("{:8.2f}".format, value)] for key, value in data.items()]
   
    table = tabulate(rows, headers=headers, tablefmt="grid")
    logger.info("\n" + table)
 

def logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt=True, result_folder_name="results", path=None):
    """
    Logs suspension kinematics simulation parameters and system information.
    This function sets up a logger, logs system and library version information, 
    and records the initial geometry data and simulation parameters for a suspension 
    kinematics analysis. Optionally, results can be saved to a text file in a specified folder.
    Parameters
    ----------
    data : dict
        Dictionary containing the initial geometry data for the suspension system.
    max_height_increase : float
        Maximum increase in suspension height to simulate.
    max_height_decrease : float
        Maximum decrease in suspension height to simulate.
    height_step : float
        Step size for height changes during the simulation.
    save_to_txt : bool, optional
        Whether to save the results to a text file (default is True).
    result_folder_name : str, optional
        Name of the folder where results will be saved (default is "results").
    path : str or None, optional
        Path to the directory where the results folder will be created (default is None).
    Returns
    -------
    None
        This function logs information but does not return any value.
    """
    logger = set_logger(result_folder_name)
    log_system_info(logger)  # log system imformation
    log_library_versions(logger)  # log Library versions
    logger.info("Initial Geometry data: ")
    logger.info("=============================================")
    log_geometry_data(logger, data)
    
    logger.info("Range to simulate: ")
    logger.info("=============================================")
    logger.info(f"max_height_increase {max_height_increase}")
    logger.info(f"max_height_increase {max_height_decrease}")
    logger.info(f"height_step {height_step}")
    logger.info(f"save_to_txt {save_to_txt}")
    logger.info(f"result_folder_name {result_folder_name}")
    