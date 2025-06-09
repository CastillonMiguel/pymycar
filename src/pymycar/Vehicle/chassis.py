"""
Chassis Class
=============

The `Chassis` class represents the physical properties and state of the vehicle's chassis in the simulation. 
It includes geometric dimensions, mass, inertia properties, and aerodynamic characteristics.

.. code-block::

    #
    #       |<--rear_axle_to_com-->|<--front_axle_to_com-->|
    #
    #       |.....|
    #   |---|.....|-------------\  |                       |
    #   |     / \                \-----------------------|...|--------|   ---
    #   |      |                                                      |   / \ 
    #   |      |                                                      |    |   
    #   |      |                                                      |    |
    #   |      |                   com                                |    |
    #   |  rear_track              *                                  |   front_track   
    #   |      |                                                      |    |
    #   |      |                                                      |    |
    #   |      |                                                      |    |
    #   |      |                                                      |   \ /
    #   |     \ /                /-----------------------|...|--------|   ---
    #   |---|.....|-------------/                    
    #       |.....|
    #
    #


+-------------------+------------------------------------------------------+
| Parameter         | Description                                          |
+===================+======================================================+
| front_axle_to_com | distance between the front axle and the vehicle CoM  |
+-------------------+------------------------------------------------------+
| rear_axle_to_com  | distance between the rear axle and the vehicle CoM   |
+-------------------+------------------------------------------------------+
| wheelbase         | front_axle_to_com + rear_axle_to_com                 |
+-------------------+------------------------------------------------------+
| front_track       | front track                                          |
+-------------------+------------------------------------------------------+
| rear_track        | rear track                                           |
+-------------------+------------------------------------------------------+
| com_height        | CoM height                                           |
+-------------------+------------------------------------------------------+
| total_mass        | total mass of the chassis                            |
+-------------------+------------------------------------------------------+
| inertia_x         | x-axis vehicle inertia (w.r.t. CoM)                  |
+-------------------+------------------------------------------------------+
| inertia_y         | y-axis vehicle inertia (w.r.t. CoM)                  |
+-------------------+------------------------------------------------------+
| inertia_z         | z-axis vehicle inertia (w.r.t. CoM)                  |
+-------------------+------------------------------------------------------+
| drag_coefficient  | aerodynamics drag coefficient                        |
+-------------------+------------------------------------------------------+
| lift_coefficient  | aerodynamics lift coefficient                        |
+-------------------+------------------------------------------------------+


"""

from pymycar.files import append_results_to_file
class Chassis:
    """
    The `Chassis` class represents the physical properties and state of the vehicle's chassis in the simulation. 
    It includes geometric dimensions, mass, inertia properties, and aerodynamic characteristics.

    Attributes
    ----------
    front_axle_to_com : float
        The distance between the front axle and the vehicle's center of mass (CoM). (default: 1.48 m)
    rear_axle_to_com : float
        The distance between the rear axle and the vehicle's center of mass (CoM). (default: 1.12 m)
    wheelbase : float
        The total distance between the front and rear axles. It is the sum of `front_axle_to_com` and `rear_axle_to_com`.
    front_track : float
        The width of the chassis at the front axle, representing the distance between the left and right front wheels. (default: 1.71 m)
    rear_track : float
        The width of the chassis at the rear axle, representing the distance between the left and right rear wheels. (default: 1.62 m)
    com_height : float
        The height of the center of mass (CoM) from the ground. (default: 0.4 m)
    mass : float
        The total mass of the chassis. (default: 1400 kg)
    inertia_x : float
        The moment of inertia about the x-axis (roll axis) of the vehicle, with respect to the CoM. (default: 400 kg·m²)
    inertia_y : float
        The moment of inertia about the y-axis (pitch axis) of the vehicle, with respect to the CoM. (default: 2000 kg·m²)
    inertia_z : float
        The moment of inertia about the z-axis (yaw axis) of the vehicle, with respect to the CoM. (default: 1320 kg·m²)
    drag_coefficient : float
        The drag coefficient used for aerodynamic calculations. (default: 0.34)
    lift_coefficient : float
        The lift coefficient used for aerodynamic calculations. (default: 0.0)

    Methods
    -------
    __init__(front_axle_to_com, rear_axle_to_com, front_track, rear_track, com_height, mass, inertia_x, inertia_y, inertia_z, drag_coefficient, lift_coefficient)
        Initializes the chassis with the specified or default parameters.

    update_state(dt)
        Updates the chassis's position and orientation based on the velocity and angular velocity for the given time step (`dt`).

    save_state()
        Saves the current state of the chassis, including CAD data, at the current simulation step.

    set_velocity(vx, vy, vz, roll_rate, pitch_rate, yaw_rate)
        Sets the chassis's linear and angular velocities, including both translational and rotational components.

    print_info()
        Prints the current state of the chassis, including its position, orientation, velocity, and angular velocity.

    update_chassis_data(**kwargs)
        Updates chassis parameters dynamically based on the provided keyword arguments.

    save_log_info(logger)
        Logs the chassis parameters in a tabular format using the provided logger instance.
    """

    def __init__(
        self, 
        front_axle_to_com=None,
        rear_axle_to_com=None,
        front_track=None,
        rear_track=None,
        com_height=None,
        mass=None,
        inertia_x=None,
        inertia_y=None,
        inertia_z=None,
        drag_coefficient=None,
        lift_coefficient=None
    ):
        """
        Initializes the chassis with the specified or default parameters.

        Parameters
        ----------
        front_axle_to_com : float, optional
            The distance between the front axle and the center of mass (CoM) of the vehicle (default: 1.48 m).
        rear_axle_to_com : float, optional
            The distance between the rear axle and the center of mass (CoM) of the vehicle (default: 1.12 m).
        front_track : float, optional
            The width of the vehicle at the front axle (default: 1.71 m).
        rear_track : float, optional
            The width of the vehicle at the rear axle (default: 1.62 m).
        com_height : float, optional
            The height of the center of mass from the ground (default: 0.4 m).
        mass : float, optional
            The total mass of the chassis (default: 1400 kg).
        inertia_x : float, optional
            Moment of inertia about the x-axis (roll axis) relative to the CoM (default: 400 kg·m²).
        inertia_y : float, optional
            Moment of inertia about the y-axis (pitch axis) relative to the CoM (default: 2000 kg·m²).
        inertia_z : float, optional
            Moment of inertia about the z-axis (yaw axis) relative to the CoM (default: 1320 kg·m²).
        drag_coefficient : float, optional
            The drag coefficient used for aerodynamic calculations (default: 0.34).
        lift_coefficient : float, optional
            The lift coefficient used for aerodynamic calculations (default: 0.0).
        """
        # Geometry
        self.front_axle_to_com = front_axle_to_com
        self.rear_axle_to_com = rear_axle_to_com
        # Only calculate wheelbase if both front_axle_to_com and rear_axle_to_com are not None
        if front_axle_to_com is not None and rear_axle_to_com is not None:
            self.wheelbase = front_axle_to_com + rear_axle_to_com
        else:
            self.wheelbase = None
        self.front_track = front_track
        self.rear_track = rear_track
        
        self.com_height = com_height
        
        # Mass
        self.mass = mass
        
        # Inertia
        self.inertia_x = inertia_x
        self.inertia_y = inertia_y
        self.inertia_z = inertia_z
        
        # Aerodynamics
        self.drag_coefficient = drag_coefficient
        self.lift_coefficient = lift_coefficient
        
        self.time = 0.0
        
        # Initial chassis state (position and orientation)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        
        # Initial chassis velocity and angular velocity
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.roll_rate = 0.0
        self.pitch_rate = 0.0
        self.yaw_rate = 0.0
        
    def update_state(self, dt):
        """
        Updates the chassis's position and orientation based on the velocity and angular velocity for the given time step (`dt`).

        Parameters
        ----------
        dt : float
            The time step used for updating the chassis's state.
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        self.roll += self.roll_rate * dt
        self.pitch += self.pitch_rate * dt
        self.yaw += self.yaw_rate * dt
    
    # def save_state(self):
    #     """
    #     Saves the current state of the chassis, including CAD data, at the current simulation step.
    #     """
    #     self.set_cad()
    #     file_name = f"chassis_cad_{self.step}.vtm"
    #     time_step = self.cad
    #     time_step.save("solution/"+file_name)
    #     self.step += 1

    def set_velocity(self, vx, vy, vz, roll_rate, pitch_rate, yaw_rate):
        """
        Sets the chassis's linear and angular velocities, including both translational and rotational components.

        Parameters
        ----------
        vx : float
            The linear velocity along the x-axis.
        vy : float
            The linear velocity along the y-axis.
        vz : float
            The linear velocity along the z-axis.
        roll_rate : float
            The angular velocity around the x-axis (roll).
        pitch_rate : float
            The angular velocity around the y-axis (pitch).
        yaw_rate : float
            The angular velocity around the z-axis (yaw).
        """
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.roll_rate = roll_rate
        self.pitch_rate = pitch_rate
        self.yaw_rate = yaw_rate
    
    def save_state_2_text_file(self, output_file_path):
        header = '#time\tx\ty\tz\troll\tpitch\tyaw\tvx\tvy\tvz\troll_rate\tpitch_rate\tyaw_rate'
        append_results_to_file(output_file_path, header, self.time, self.x, self.y, self.z,self.roll, self.pitch, self.yaw, self.vx, self.vy, self.vz,self.roll_rate, self.pitch_rate, self.yaw_rate)
        
    def print_info(self):
        """
        Prints the current state of the chassis, including its position, orientation, velocity, and angular velocity.
        """
        print(f"Chassis State:")
        print(f"Position (x, y, z): ({self.x}, {self.y}, {self.z})")
        print(f"Orientation (roll, pitch, yaw): ({self.roll}, {self.pitch}, {self.yaw})")
        print(f"Velocity (vx, vy, vz): ({self.vx}, {self.vy}, {self.vz})")
        print(f"Angular Velocity (roll_rate, pitch_rate, yaw_rate): ({self.roll_rate}, {self.pitch_rate}, {self.yaw_rate})")


    def update_chassis_data(self, **kwargs):
        """
        Updates chassis parameters dynamically based on the provided keyword arguments.

        Parameters
        ----------
        **kwargs : dict
            A dictionary of parameters to update in the chassis model.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Attribute {key} does not exist in CarChassis.")
                
    def save_log_info(self, logger):
        """
        Logs the chassis parameters in a tabular format using the provided logger instance.

        Parameters
        ----------
        logger : logging.Logger
            An instance of a logger object to record the chassis parameters.
        """
        data = [
            ("front_axle_to_com", f"{self.front_axle_to_com}"),
            ("rear_axle_to_com", f"{self.rear_axle_to_com}"),
            ("wheelbase", f"{self.front_axle_to_com + self.rear_axle_to_com}"),
            ("front_track", f"{self.front_track}"),
            ("rear_track", f"{self.rear_track}"),
            ("com_height", f"{self.com_height}"),
            ("total_mass", f"{self.mass}"),
            ("inertia_x", f"{self.inertia_x}"),
            ("inertia_y", f"{self.inertia_y}"),
            ("inertia_z", f"{self.inertia_z}"),
            ("drag_coefficient", f"{self.drag_coefficient}"),
            ("lift_coefficient", f"{self.lift_coefficient}"),
        ]

        # Create the table header
        logger.info("Chassis Parameters")
        logger.info("================================================")
        logger.info("+-------------------+--------------------------+")
        logger.info("| Parameter         | Value                    |")
        logger.info("+===================+==========================+")

        # Log each row of the table
        for param, value in data:
            logger.info(f"| {param:<17} | {value:<24} |")
            logger.info("+-------------------+--------------------------+")
            
            
            
        # # Visualization
        # self.cad = None
        # self.type_visualization_cad = "tourist_chassiss"
        
        # self.step = 0
        
        #     def set_cad(self):
        # if self.type_visualization_cad == "tourist_chassis":
        #     self.cad = tourist_chassis(
        #             self.front_axle_to_com,
        #             self.rear_axle_to_com,
        #             self.front_track,
        #             self.rear_track,
        #             self.com_height,
        #             self.roll,
        #             self.pitch,
        #             self.yaw,
        #             self.x,
        #             self.y,
        #             self.z)
        # else:
        #     self.cad = model_A(
        #             self.front_axle_to_com,
        #             self.rear_axle_to_com,
        #             self.front_track,
        #             self.rear_track,
        #             self.com_height,
        #             self.roll,
        #             self.pitch,
        #             self.yaw,
        #             self.x,
        #             self.y,
        #             self.z)
