"""
Suspension Class
================

The `SimpleSuspension` class represents the properties of a suspension system in a vehicle model. 
This class models the basic dynamics of the suspension, including the stiffness and damping characteristics.

"""

class SimpleSuspension:
    """
    Represents a simple suspension system with basic properties: stiffness and damping.

    Attributes
    ----------
    stiffness : float
        The stiffness of the suspension in N/m. This value defines how much force the suspension applies to resist compression or extension.
    damper : float
        The damping coefficient in Ns/m. This value defines the resistance the suspension provides against motion, simulating viscous friction.

    Methods
    -------
    __init__(stiffness, damper)
        Initializes the suspension system with the specified stiffness and damping values.
        
    save_log_info(logger, name="Suspension")
        Logs the suspension parameters in a tabular format using the provided logger.
    """

    def __init__(
        self,
        stiffness=None,
        damper=None
    ):
        """
        Initializes the SimpleSuspension object with provided stiffness and damper values.

        Parameters
        ----------
        stiffness : float, optional
            The stiffness of the suspension in N/m. Defines how much resistance the suspension provides to compression or extension (default: 1).
        damper : float, optional
            The damping coefficient in Ns/m. Represents the resistance of the suspension to motion through viscous damping (default: 1).
        """
        self.stiffness = stiffness
        self.damper = damper
        
    def save_log_info(self, logger, name="Suspension"):
        """
        Logs the suspension parameters in a tabular format using the provided logger.

        Parameters
        ----------
        logger : logging.Logger
            The logger instance that will be used to log the suspension details.
        name : str, optional
            Custom name for the suspension system (default: "Suspension").
        """
        data = [
            ("stiffness", f"{self.stiffness}"),
            ("damper", f"{self.damper}"),
        ]

        # Create the table header
        logger.info("Suspension Parameters: " + name)
        logger.info("================================================")
        logger.info("+---------------------------+--------------------------+")
        logger.info("| Parameter                 | Value                    |")
        logger.info("+===========================+==========================+")

        # Log each row of the table
        for param, value in data:
            logger.info(f"| {param:<25} | {value:<24} |")
            logger.info("+---------------------------+--------------------------+")


class Suspension:
    def __init__(
        self,
        kinematics
    ):
        self.cad = False #kinematics.set_cad(1)
        