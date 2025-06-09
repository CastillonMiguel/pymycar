"""
MyCar Class
===========

The `MyCar` class represents a complete vehicle dynamics simulation model. 
It integrates various subsystems essential for vehicle behavior simulation, 
including the chassis, wheels, and suspension components.

The class is composed of the following subclasses:

- **Chassis**: Represents the main body of the vehicle, including mass, dimensions, and inertia properties.
- **Wheel**: Four instances of the `Wheel` class represent the front-left, front-right, rear-left, and rear-right wheels.
- **Suspension**: Four instances of the `Suspension` class simulate the dynamic response of the suspension system at each wheel.


"""

from pymycar.files import prepare_simulation

import os
class MyCar:
    """
    The `MyCar` class integrates the vehicle dynamics subsystems: chassis, wheels, and suspensions.
    
    Attributes
    ----------
    chassis : Chassis
        Represents the main vehicle body.
    left_rear_wheel : Wheel
        Instance of the `Wheel` class for the rear-left wheel.
    right_rear_wheel : Wheel
        Instance of the `Wheel` class for the rear-right wheel.
    left_front_wheel : Wheel
        Instance of the `Wheel` class for the front-left wheel.
    right_front_wheel : Wheel
        Instance of the `Wheel` class for the front-right wheel.
    left_rear_suspension : Suspension
        Instance of the `Suspension` class for the rear-left suspension.
    right_rear_suspension : Suspension
        Instance of the `Suspension` class for the rear-right suspension.
    left_front_suspension : Suspension
        Instance of the `Suspension` class for the front-left suspension.
    right_front_suspension : Suspension
        Instance of the `Suspension` class for the front-right suspension.

    Methods
    -------
    __init__(chassis, left_rear_wheel, right_rear_wheel, left_front_wheel, right_front_wheel, left_rear_suspension, right_rear_suspension, left_front_suspension, right_front_suspension)
        Initializes the MyCar instance with provided subsystem objects.

    save_log_info(logger)
        Logs the simulation parameters of the vehicle and its subsystems.
    """

    def __init__(
        self, 
        chassis=None,
        left_rear_wheel=None,
        right_rear_wheel=None,
        left_front_wheel=None,
        right_front_wheel=None,
        left_rear_suspension=None,
        right_rear_suspension=None,
        left_front_suspension=None,
        right_front_suspension=None,
        path=None,
        result_folder_name="results"
    ):
        """
        Initialize the `MyCar` instance with provided subsystem objects.

        Parameters
        ----------
        chassis : Chassis, optional
            Instance of the `Chassis` class (default is None).
        left_rear_wheel : Wheel, optional
            Instance of the `Wheel` class for the rear-left wheel (default is None).
        right_rear_wheel : Wheel, optional
            Instance of the `Wheel` class for the rear-right wheel (default is None).
        left_front_wheel : Wheel, optional
            Instance of the `Wheel` class for the front-left wheel (default is None).
        right_front_wheel : Wheel, optional
            Instance of the `Wheel` class for the front-right wheel (default is None).
        left_rear_suspension : Suspension, optional
            Instance of the `Suspension` class for the rear-left suspension (default is None).
        right_rear_suspension : Suspension, optional
            Instance of the `Suspension` class for the rear-right suspension (default is None).
        left_front_suspension : Suspension, optional
            Instance of the `Suspension` class for the front-left suspension (default is None).
        right_front_suspension : Suspension, optional
            Instance of the `Suspension` class for the front-right suspension (default is None).
        """
        
        self.result_folder_name = result_folder_name
        self.path = path
        # if self.path is None:
        #     self.path = os.getcwd()
        # else:
        #     self.path = path
        
        #prepare_simulation(self.path, self.result_folder_name)
        
        # Chassis
        self.chassis = chassis

        # Wheels
        self.left_rear_wheel = left_rear_wheel
        self.right_rear_wheel = right_rear_wheel
        self.left_front_wheel = left_front_wheel
        self.right_front_wheel = right_front_wheel

        # Suspensions
        self.left_rear_suspension = left_rear_suspension
        self.right_rear_suspension = right_rear_suspension
        self.left_front_suspension = left_front_suspension
        self.right_front_suspension = right_front_suspension
        
    def save_state_2_text_file(self):
        self.chassis.save_state_2_text_file(os.path.join(self.path, self.result_folder_name, "chassis.dof"))
        
        self.left_rear_wheel.save_state_2_text_file(os.path.join(self.path, self.result_folder_name, "left_rear_wheel.dof"))
        self.right_rear_wheel.save_state_2_text_file(os.path.join(self.path, self.result_folder_name, "right_rear_wheel.dof"))
        self.left_front_wheel.save_state_2_text_file(os.path.join(self.path, self.result_folder_name, "left_front_wheel.dof"))
        self.right_front_wheel.save_state_2_text_file(os.path.join(self.path, self.result_folder_name, "right_front_suspension.dof"))
        
        
    def save_log_info(self, logger):
        """
        Log the simulation parameters of the vehicle and its subsystems.

        Parameters
        ----------
        logger : logging.Logger
            An instance of a logger to log the details.
        
        Notes
        -----
        The logger outputs detailed information for the following components:
        - Chassis
        - Each of the four wheels
        - Each of the four suspension systems
        """
        logger.info(" ")
        logger.info("********************************************************")
        logger.info("* MyCar Parameters *************************************")
        logger.info("********************************************************")
        logger.info(" ")

        # Log Chassis Info
        if self.chassis:
            self.chassis.save_log_info(logger)
        else:
            logger.info("Chassis information not provided.")
        
        logger.info(" ")

        # Log Wheel Info
        wheels = {
            "left rear wheel": self.left_rear_wheel,
            "right rear wheel": self.right_rear_wheel,
            "left front wheel": self.left_front_wheel,
            "right front wheel": self.right_front_wheel,
        }
        for name, wheel in wheels.items():
            if wheel:
                wheel.save_log_info(logger, name)
            else:
                logger.info(f"{name} information not provided.")
            logger.info(" ")

        # Log Suspension Info
        suspensions = {
            "left rear suspension": self.left_rear_suspension,
            "right rear suspension": self.right_rear_suspension,
            "left front suspension": self.left_front_suspension,
            "right front suspension": self.right_front_suspension,
        }
        for name, suspension in suspensions.items():
            if suspension:
                suspension.save_log_info(logger, name)
            else:
                logger.info(f"{name} information not provided.")
            logger.info(" ")



    #     # view ####
    #     self.left_rear_wheel.x = -self.chassis.rear_axle_to_com
    #     self.left_rear_wheel.y = -self.chassis.rear_track
    #     self.left_rear_wheel.z = 0.0
        
    #     self.right_rear_wheel.x = -self.chassis.rear_axle_to_com
    #     self.right_rear_wheel.y =  self.chassis.rear_track
    #     self.right_rear_wheel.z = 0.0
        
    #     self.left_front_wheel.x = +self.chassis.front_axle_to_com
    #     self.left_front_wheel.y = -self.chassis.front_track
    #     self.left_front_wheel.z = 0.0
        
    #     self.right_front_wheel.x = +self.chassis.front_axle_to_com
    #     self.right_front_wheel.y = +self.chassis.front_track
    #     self.right_front_wheel.z = 0.0
    #     ######
        
    #     self.cad = None
    
    # def set_cad(self):
    #      self.chassis.set_cad()
    #      self.left_rear_wheel.set_cad()
    #      self.right_rear_wheel.set_cad()
    #      self.left_front_wheel.set_cad()
    #      self.right_front_wheel.set_cad()
    #      self.cad = pv.MultiBlock([self.chassis.cad, 
    #                                self.left_rear_wheel.cad,
    #                                self.right_rear_wheel.cad,
    #                                self.left_front_wheel.cad,
    #                                self.right_front_wheel.cad])
        
    # def view_cad(self):
    #     if self.cad == None:
    #         self.set_cad()
        
    #     plotter = pv.Plotter()
    #     plotter.add_mesh(self.chassis.cad, color ="red", show_edges=True)
    #     plotter.add_mesh(self.left_rear_wheel.cad, color ="black", show_edges=True)
    #     plotter.add_mesh(self.right_rear_wheel.cad, color ="black", show_edges=True)
    #     plotter.add_mesh(self.left_front_wheel.cad, color ="black", show_edges=True)
    #     plotter.add_mesh(self.right_front_wheel.cad, color ="black", show_edges=True)
        
    #     # if self.left_rear_suspension!=None:
    #     #     plotter.add_mesh(self.left_rear_suspension.cad, color ="blue", show_edges=True)
    #     # if self.right_rear_suspension!=None:
    #     #     plotter.add_mesh(self.right_rear_suspension.cad, color ="yellow", show_edges=True)
            
    #     plotter.show()
