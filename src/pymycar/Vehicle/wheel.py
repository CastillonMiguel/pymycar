"""
Wheel Class
===========

The `Wheel` class represents the properties and dynamics of a single wheel in a vehicle model. 
This includes physical parameters such as mass, stiffness, and adherence properties, 
as well as the wheel's position and orientation in 3D space.

"""

from pymycar.files import append_results_to_file

class Wheel:
    """
    Represents a single wheel in the vehicle model with its physical and dynamic properties.
    
    Attributes
    ----------
    mass : float
        Mass of the wheel in kilograms.
    spin_inertia : float
        Moment of inertia for spinning motion in kg·m².
    nominal_radius : float
        Nominal radius of the wheel in meters.
    radial_stiffness : float
        Radial stiffness of the wheel in N/m.
    radial_damping : float
        Radial damping coefficient of the wheel in Ns/m.
    nominal_vertical_load : float
        Nominal vertical load supported by the wheel in N.
    max_longitudinal_adherence : float
        Maximum longitudinal adherence coefficient.
    max_lateral_adherence : float
        Maximum lateral adherence coefficient.
    sidelsip_stiffness : float
        Side-slip stiffness in N/deg.
    longitudinal_stiffness : float
        Longitudinal stiffness in N/deg.
    x : float
        X-coordinate position of the wheel.
    y : float
        Y-coordinate position of the wheel.
    z : float
        Z-coordinate position of the wheel.
    camber : float
        Camber angle of the wheel in degrees.
    toe : float
        Toe angle of the wheel in degrees.
    side_view : float
        Side view tilt angle of the wheel in degrees.

    Methods
    -------
    __init__(mass, spin_inertia, nominal_radius, radial_stiffness, radial_damping, nominal_vertical_load, max_longitudinal_adherence, max_lateral_adherence, sidelsip_stiffness, longitudinal_stiffness)
        Initializes the Wheel object with provided or default parameters.

    save_log_info(logger, name="Wheel")
        Logs the wheel's parameters in a tabular format.
    """

    def __init__(self, 
                 mass=None,
                 spin_inertia=None,
                 nominal_radius=None,
                 radial_stiffness=None,
                 radial_damping=None,
                 nominal_vertical_load=None,
                 max_longitudinal_adherence=None,
                 max_lateral_adherence=None,
                 sidelsip_stiffness=None,
                 longitudinal_stiffness=None):
        """
        Initializes the Wheel object with physical and position parameters.

        Parameters
        ----------
        mass : float, optional
            Mass of the wheel in kilograms (default: 15.0).
        spin_inertia : float, optional
            Moment of inertia for spinning motion in kg·m² (default: 1.3).
        nominal_radius : float, optional
            Nominal radius of the wheel in meters (default: 0.29).
        radial_stiffness : float, optional
            Radial stiffness of the wheel in N/m (default: 200,000.0).
        radial_damping : float, optional
            Radial damping coefficient of the wheel in Ns/m (default: 150.0).
        nominal_vertical_load : float, optional
            Nominal vertical load supported by the wheel in N (default: 5000.0).
        max_longitudinal_adherence : float, optional
            Maximum longitudinal adherence coefficient (default: 1.57).
        max_lateral_adherence : float, optional
            Maximum lateral adherence coefficient (default: 1.41).
        sidelsip_stiffness : float, optional
            Side-slip stiffness in N/deg (default: 25.0).
        longitudinal_stiffness : float, optional
            Longitudinal stiffness in N/deg (default: 34.0).
        """
        
        self.time = 0.0
        # Initialize position and orientation
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.camber = 0.0
        self.toe = 0.0
        self.side_view = 0.0

        # Initialize physical properties
        self.mass = mass
        self.spin_inertia = spin_inertia
        self.nominal_radius = nominal_radius
        self.radial_stiffness = radial_stiffness
        self.radial_damping = radial_damping
        self.nominal_vertical_load = nominal_vertical_load
        self.max_longitudinal_adherence = max_longitudinal_adherence
        self.max_lateral_adherence = max_lateral_adherence
        self.sidelsip_stiffness = sidelsip_stiffness
        self.longitudinal_stiffness = longitudinal_stiffness

    def save_state_2_text_file(self, output_file_path):
        header = '#time\tx\ty\tz\tcamber\ttoe\tside_view'
        append_results_to_file(output_file_path, header, self.time, self.x, self.y, self.z,self.camber, self.toe, self.side_view)
        
    def save_log_info(self, logger, name="Wheel"):
        """
        Logs the wheel parameters in a tabular format using the provided logger.

        Parameters
        ----------
        logger : logging.Logger
            Logger instance for logging the wheel details.
        name : str, optional
            Name or identifier for the wheel (default: "Wheel").
        """
        data = [
            ("mass", f"{self.mass}"),
            ("spin_inertia", f"{self.spin_inertia}"),
            ("nominal_radius", f"{self.nominal_radius}"),
            ("radial_stiffness", f"{self.radial_stiffness}"),
            ("radial_damping", f"{self.radial_damping}"),
            ("nominal_vertical_load", f"{self.nominal_vertical_load}"),
            ("max_longitudinal_adherence", f"{self.max_longitudinal_adherence}"),
            ("max_lateral_adherence", f"{self.max_lateral_adherence}"),
            ("sidelsip_stiffness", f"{self.sidelsip_stiffness}"),
            ("longitudinal_stiffness", f"{self.longitudinal_stiffness}"),
        ]

        # Create the table header
        logger.info("Wheel Parameters: " + name)
        logger.info("================================================")
        logger.info("+---------------------------+--------------------------+")
        logger.info("| Parameter                 | Value                    |")
        logger.info("+===========================+==========================+")

        # Log each row of the table
        for param, value in data:
            logger.info(f"| {param:<25} | {value:<24} |")
            logger.info("+---------------------------+--------------------------+")
            

#         # self.wheel_base =
#         # self.wheel_track = 
#         # self.wheel_jounce = 
#         # self.caster_angle = 
#         # self.kingpin_angle =
#         # self.camber_angle = 



    #     self.cad = None
        
        
    # def set_cad(self):
    #     wheel = pv.Cylinder(center=(self.x, self.y, self.z), direction=(0, 1, 0), height=0.5*self.nominal_radius, radius = self.nominal_radius)
    #     wheel = wheel.rotate_x(np.rad2deg(self.camber))
    #     wheel = wheel.rotate_y(np.rad2deg(self.toe))
    #     wheel = wheel .rotate_z(np.rad2deg(self.side_view))
    #     self.cad = pv.MultiBlock([wheel])
        
    # def view_cad(self):
    #     if self.cad == None:
    #         self.set_cad()
        
    #     plotter = pv.Plotter()
    #     plotter.add_mesh(self.cad, color='black', show_edges=True)
    #     plotter.show()
    