import numpy as np
import matplotlib.pyplot as plt
import scipy
import os
from pymycar.files import prepare_simulation, append_results_to_file
from pymycar.Logger.library_versions import set_logger, log_library_versions, log_system_info, log_end_analysis#, log_model_information

def solver(system, time_points, initial_conditions):
    """
     Solve the differential equations.

    Returns:
    --------
    np.ndarray
        Solution array.
    """
    solution = scipy.integrate.solve_ivp(system,
                        (np.min(time_points), np.max(time_points)),
                         initial_conditions,
                         method = 'RK45',
                         t_eval = time_points,
                         max_step = np.min(np.diff(time_points)))
    return solution
       




#     --------------------     ^
#     |                  |     | zs
#     |        ms        |    --- 
#     |                  |    
#     --------------------
#           \       |
#       k1  /      |_| c1
#           \       |
#        ---------------       ^
#        |             |       | zu
#        |     mu      |      ---
#        |             |      
#        ---------------
#           \       |
#       kw1 /      |_| cw1
#           \       |
#           ---------
#             \   /
#               *      __      __
#       ______________/  \    /  \_________
#                         \__/
class VerticalQuarterCar:
    """
    Simulate a vertical quarter car model and save results to a text file.

    Parameters:
    ----------
    custom_excitation : function
        Custom excitation function.
    time_points : array-like
        Time points for simulation.

    Attributes:
    ----------
    number_dofs : int
        Number of degrees of freedom (constant).

    Methods:
    --------
    get_mass_matrix()
    get_damper_matrix()
    get_stiffness_matrix()
    get_F_vector(t)
    system(y, t)
    solve()
    save_2_text_file()
    plot_results()
    """

    number_dofs = 2

    def __init__(self, mycar, quarter_part="right_front", result_folder_name="results", path = None):
        """
        Initialize the VerticalQuarterCar object.

        Parameters:
        ----------
        custom_excitation : function
            Custom excitation function.
        time_points : array-like
            Time points for simulation.
        """
        
        self.result_folder_name = result_folder_name
        if path is None:
            path = os.getcwd()
        
        prepare_simulation(path, self.result_folder_name)
        # logger_suspension_kinematics(data, max_height_increase, max_height_decrease, height_step, save_to_txt, result_folder_name, path)
        logger = set_logger(self.result_folder_name)
        log_system_info(logger)  # log system imformation
        log_library_versions(logger)  # log Library versions
        
        # Parameters
        self.ms = mycar.chassis.mass/4
        
        if quarter_part == "right_front":
            self.mu = mycar.right_front_wheel.mass
            self.c1 = mycar.right_front_suspension.damper
            self.k1 = mycar.right_front_suspension.stiffness
            self.cw1 = mycar.right_front_wheel.radial_damping
            self.kw1 = mycar.right_front_wheel.radial_stiffness
            
        elif quarter_part == "left_front":
            self.mu = mycar.left_front_wheel.mass
            self.c1 = mycar.left_front_suspension.damper
            self.k1 = mycar.left_front_suspension.stiffness
            self.cw1 = mycar.left_front_wheel.radial_damping
            self.kw1 = mycar.left_front_wheel.radial_stiffness
            
        elif quarter_part == "right_rear":
            self.mu = mycar.right_rear_wheel.mass
            self.c1 = mycar.right_rear_suspension.damper
            self.k1 = mycar.right_rear_suspension.stiffness
            self.cw1 = mycar.right_rear_wheel.radial_damping
            self.kw1 = mycar.right_rear_wheel.radial_stiffness
            
        elif quarter_part == "left_rear":
            self.mu = mycar.left_rear_wheel.mass
            self.c1 = mycar.left_rear_suspension.damper
            self.k1 = mycar.left_rear_suspension.stiffness
            self.cw1 = mycar.left_rear_wheel.radial_damping
            self.kw1 = mycar.left_rear_wheel.radial_stiffness
            
        else:
            print("Invalid quarter part. Choose between 'right_front', 'left_front', 'right_rear', 'left_rear'")

        
        # Mass, damping, and stiffness matrices
        self.M = self.get_mass_matrix()
        self.C = self.get_damper_matrix()
        self.K = self.get_stiffness_matrix()

        mycar.chassis.x = 0
        mycar.chassis.y = 0
        mycar.chassis.z = 0
        
        # Initial conditions: 
        self.zs_time0 = 0
        self.zs_dot_time0 = 0
        self.zu_time0 = 0
        self.zu_dot_time0 = 0

        self.initial_conditions = np.array([self.zs_time0,
                                            self.zs_dot_time0,
                                            self.zu_time0,
                                            self.zu_dot_time0])
        self.time_points = None
        
        # Wheel excitation
        self.wheel_excitation = None
        self.wheel_excitation_dot = None
        
        # Results variables
        self.zs = None
        self.zu = None
        self.zu_dot = None
        self.zs_dot = None

    def get_mass_matrix(self):
        """
        Get the mass matrix.

        Returns:
        -------
        np.ndarray
            Mass matrix.
        """
        M = np.zeros([self.number_dofs, self.number_dofs])
        M[0, 0] = self.ms
        M[1, 1] = self.mu
        return M

    def get_damper_matrix(self):
        """
        Get the damper matrix.

        Returns:
        -------
        np.ndarray
            Damper matrix.
        """
        C = np.zeros([self.number_dofs, self.number_dofs])
        C[0, 0] = self.c1
        C[1, 0] = -self.c1
        C[1, 1] = self.c1 + self.cw1
        C[0, 1] = -self.c1
        return C

    def get_stiffness_matrix(self):
        """
        Get the stiffness matrix.

        Returns:
        -------
        np.ndarray
            Stiffness matrix.
        """
        K = np.zeros([self.number_dofs, self.number_dofs])
        K[0, 0] = self.k1
        K[1, 0] = -self.k1
        K[1, 1] = self.k1 + self.kw1
        K[0, 1] = -self.k1
        return K

    def natural_frequencies(self):
        #self.eigenvalues, self.eigenvectors = np.linalg.eig(np.dot(np.linalg.inv(self.M), self.K))
        self.eigenvalues, self.eigenvectors = scipy.linalg.eig(self.K, self.M)
        self.natural_frequencies_hz = np.sqrt(self.eigenvalues) / (2 * np.pi)
        
    def get_F_vector(self, t):
        """
        Get the force vector at time t.

        Parameters:
        ----------
        t : float
            Current time.

        Returns:
        -------
        np.ndarray
            Force vector.
        """
        F = np.zeros(self.number_dofs)
        F[1] = self.kw1 * self.wheel_excitation(t)
        return F

    def system(self, t, y):
        """
        System of differential equations.

        Parameters:
        ----------
        y : np.ndarray
            State vector.
        t : float
            Current time.

        Returns:
        -------
        np.ndarray
            Derivative of the state vector.
        """
        q, q_dot = np.split(y, 2)
        F = self.get_F_vector(t)
        q_dotdot = np.linalg.solve(self.M, F - np.dot(self.C, q_dot) - np.dot(self.K, q))
        return np.concatenate((q_dot, q_dotdot))

    def solve(self):
        """
        Solve the differential equations.

        Returns:
        -------
        np.ndarray
            Solution array.
        """
        solution = solver(self.system, self.time_points, self.initial_conditions)
        
        self.zs = solution.y[0]
        self.zu = solution.y[1]
        self.zu_dot = solution.y[2]
        self.zs_dot = solution.y[3]
        self.time = solution.t
        
        self.save_2_text_file("data.txt")
        return solution

    def save_2_text_file(self, filename='data.txt'):
        """
        Save results to a text file.

        Parameters:
        ----------
        filename : str, optional
            Name of the output text file (default is 'data.txt').
        """
        # Combine arrays into one 2D array
        combined_array = np.column_stack((self.time, self.zs, self.zu, self.zu_dot, self.zs_dot))

        # Add a header
        header = "time, zs, zu, zu_dot, zs_dot "

        # Save to a text file
        np.savetxt(os.path.join(self.result_folder_name, filename), combined_array, delimiter=' ', header=header)


class VerticalHalfCar:

    number_dofs = 4 

    def __init__(self, mycar,custom_excitation, time_points, part="front"):
        
        self.time_points = time_points
        
        self.ms = mycar.chassis.mass/2
        self.Is = mycar.chassis.inertia_y
        
        self.mu1 = mycar.right_front_wheel.mass
        self.mu2 = mycar.left_front_wheel.mass
        
        self.c1 = mycar.right_front_suspension.damper
        self.c2 = mycar.left_front_suspension.damper
        self.cw1 = mycar.right_front_wheel.radial_damping
        self.cw2 = mycar.left_front_wheel.radial_damping
        
        self.k1 = mycar.right_front_suspension.stiffness
        self.k2 = mycar.left_front_suspension.stiffness
        self.kw1 = mycar.right_front_wheel.radial_stiffness
        self.kw2 = mycar.left_front_wheel.radial_stiffness
        
        self.l1 = mycar.chassis.front_track/2
        self.l2 = mycar.chassis.front_track/2
        
        
        
        self.M = self.get_mass_matrix()
        self.C = self.get_damper_matrix()
        self.K = self.get_stiffness_matrix()
        
        self.wheel_excitation_1 = custom_excitation
        self.wheel_excitation_2 = custom_excitation
        
        
        self.wheel_excitation = custom_excitation
        
        # Initial conditions: 
        self.z_s_initial     = 0
        self.z_s_dot_initial = 0
        self.theta_initial   = 0
        self.theta_dot_initial = 0
        self.z_u1_initial     = 0
        self.z_u1_dot_initial = 0
        self.z_u2_initial     = 0
        self.z_u2_dot_initial = 0
        
        self.initial_conditions = np.array([
                                            self.z_s_initial,
                                            self.z_s_dot_initial,
                                            self.theta_initial,
                                            self.theta_dot_initial,
                                            self.z_u1_initial,
                                            self.z_u1_dot_initial,
                                            self.z_u2_initial,
                                            self.z_u2_dot_initial
                                            ])
        
        
    
    def get_mass_matrix(self):
        M = np.zeros([self.number_dofs, self.number_dofs])
        M[0, 0] = self.ms
        M[1, 1] = self.Is
        M[2, 2] = self.mu1
        M[3, 3] = self.mu2
        return M
    
    def get_damper_matrix(self):
        C = np.zeros([self.number_dofs, self.number_dofs])
        
        C[0, 0] =  self.c1 + self.c2 
        C[0, 1] = -self.c1*self.l1 + self.c2*self.l2 
        C[0, 2] = -self.c1 
        C[0, 3] = -self.c2 
        
        C[1, 0] = C[0, 1]
        C[1, 1] = self.c1*self.l1**2 + self.c2*self.l2**2 
        C[1, 2] = self.c1*self.l1
        C[1, 3] =-self.c2*self.l2 
        
        C[2, 0] = C[0, 2]
        C[2, 1] = C[1, 2]
        C[2, 2] = self.c1 + self.cw1
        C[2, 3] = 0.0
        
        C[3, 0] = C[0, 3]
        C[3, 1] = C[1, 3]
        C[3, 2] = C[2, 3]
        C[3, 3] = self.c2 + self.cw2

        return C
    
    def get_stiffness_matrix(self):
        K = np.zeros([self.number_dofs, self.number_dofs])
        
        K[0, 0] =  self.k1 + self.k2 
        K[0, 1] = -self.k1*self.l1 + self.k2*self.l2 
        K[0, 2] = -self.k1 
        K[0, 3] = -self.k2 
        
        K[1, 0] = K[0, 1]
        K[1, 1] = self.k1*self.l1**2 + self.k2*self.l2**2 
        K[1, 2] = self.k1*self.l1
        K[1, 3] =-self.k2*self.l2 
        
        K[2, 0] = K[0, 2]
        K[2, 1] = K[1, 2]
        K[2, 2] = self.k1 + self.kw1
        K[2, 3] = 0.0
        
        K[3, 0] = K[0, 3]
        K[3, 1] = K[1, 3]
        K[3, 2] = K[2, 3]
        K[3, 3] = self.k2 + self.kw2
        return K
    
    def get_F_vector(self, t):
        F = np.zeros(self.number_dofs)
        F[2] = self.wheel_excitation(t)
        F[3] = self.wheel_excitation(t)
        return F
        
    def system(self, y, t):
        q, q_dot = np.split(y, 2)
        F = self.get_F_vector(t)
        q_dotdot = np.linalg.solve(self.M, F - np.dot(self.C, q_dot) - np.dot(self.K, q))
        return np.concatenate((q_dot, q_dotdot))
    
    def solve(self):
        solution = scipy.integrate.odeint(self.system, self.initial_conditions, self.time_points)

        self.Zs     = solution[:,0]
        self.Ztheta = solution[:,1]
        self.Zu1    = solution[:, 2]
        self.Zu2    = solution[:, 3]
        
        self.Zs_dot  = solution[:,4]
        self.Ztheta_dot = solution[:,5]
        self.Zu1_dot = solution[:, 6]
        self.Zu2_dot = solution[:, 7]
        
        return solution
        

class VerticalCar:
    number_dofs = 7
    def __init__(self,mycar, custom_excitation, time_points):
        
        self.wheel_excitation = custom_excitation

        
        self.time_points = time_points
        
        self.ms = mycar.chassis.mass

        self.ixx = mycar.chassis.inertia_x
        self.iyy = mycar.chassis.inertia_y
        
        self.mu1 = mycar.right_front_wheel.mass
        self.mu2 = mycar.left_front_wheel.mass
        self.mu3 = mycar.right_rear_wheel.mass
        self.mu4 = mycar.left_rear_wheel.mass
        
        self.c1 = mycar.right_front_suspension.damper
        self.c2 = mycar.left_front_suspension.damper
        self.c3 = mycar.right_rear_suspension.damper
        self.c4 = mycar.left_rear_suspension.damper
        
        self.cw1 = mycar.right_front_wheel.radial_damping
        self.cw2 = mycar.left_front_wheel.radial_damping
        self.cw3 = mycar.right_rear_wheel.radial_damping
        self.cw4 = mycar.left_rear_wheel.radial_damping
        
        self.k1 = mycar.right_front_suspension.stiffness
        self.k2 = mycar.left_front_suspension.stiffness
        self.k3 = mycar.right_rear_suspension.stiffness
        self.k4 = mycar.left_rear_suspension.stiffness
        
        self.kw1 = mycar.right_front_wheel.radial_stiffness
        self.kw2 = mycar.left_front_wheel.radial_stiffness
        self.kw3 = mycar.right_rear_wheel.radial_stiffness
        self.kw4 = mycar.left_rear_wheel.radial_stiffness
        
        self.lf = mycar.chassis.front_axle_to_com
        self.lr = mycar.chassis.rear_axle_to_com
        
        self.t1 = mycar.chassis.front_track/2
        self.t2 = mycar.chassis.front_track/2
        self.t3 = mycar.chassis.rear_track/2
        self.t4 = mycar.chassis.rear_track/2
                
        self.M = self.get_mass_matrix()
        self.C = self.get_damper_matrix()
        self.K = self.get_stiffness_matrix()
        
        self.wheel_excitation_1 = custom_excitation
        self.wheel_excitation_2 = custom_excitation
        self.wheel_excitation_3 = custom_excitation
        self.wheel_excitation_4 = custom_excitation
        
        
        # Initial conditions: 
        self.z_s_initial     = 0
        self.z_s_dot_initial = 0
        self.alpha_initial   = 0
        self.alpha_dot_initial = 0
        self.beta_initial     = 0
        self.beta_dot_initial = 0
        self.z_u1_initial     = 0
        self.z_u1_dot_initial = 0
        self.z_u2_initial     = 0
        self.z_u2_dot_initial = 0
        self.z_u3_initial     = 0
        self.z_u3_dot_initial = 0
        self.z_u4_initial     = 0
        self.z_u4_dot_initial = 0
        
        self.initial_conditions = np.array([
                                            self.z_s_initial,
                                            self.z_s_dot_initial,
                                            self.alpha_initial,
                                            self.alpha_dot_initial,
                                            self.beta_initial,
                                            self.beta_dot_initial,
                                            self.z_u1_initial,
                                            self.z_u1_dot_initial,
                                            self.z_u2_initial,
                                            self.z_u2_dot_initial,
                                            self.z_u3_initial,
                                            self.z_u3_dot_initial,
                                            self.z_u4_initial,
                                            self.z_u4_dot_initial,
                                            ])
        
        
    
    def get_mass_matrix(self):
        M = np.zeros([self.number_dofs, self.number_dofs])
        M[0, 0] = self.ms
        M[1, 1] = self.ixx
        M[2, 2] = self.iyy
        M[3, 3] = self.mu1
        M[4, 4] = self.mu2
        M[5, 5] = self.mu3
        M[6, 6] = self.mu4
        return M
    
    def get_damper_matrix(self):
        C = np.zeros([self.number_dofs, self.number_dofs])
        
        C[0, 0] =  self.c1 + self.c2 + self.c3 + self.c4
        C[0, 1] =  self.c1*self.t1 - self.c2*self.t2 + self.c3*self.t3 - self.c4*self.t4
        C[0, 2] =  self.c1*self.lf + self.c2*self.lf - self.c3*self.lr - self.c4*self.lr
        C[0, 3] = -self.c1
        C[0, 4] = -self.c2
        C[0, 5] = -self.c3
        C[0, 6] = -self.c4
        
        C[1, 0] =  C[0, 1]
        C[1, 1] =  self.c1*self.t1**2 + self.c2*self.t2**2 + self.c3*self.t3**2 + self.c4*self.t4**2
        C[1, 2] =  self.c1*self.t1*self.lf + self.c2*self.t2*self.lf - self.c3*self.t3*self.lr - self.c4*self.t4*self.lr
        C[1, 3] = -self.c1*self.t1
        C[1, 4] =  self.c2*self.t2
        C[1, 5] = -self.c3*self.t3
        C[1, 6] =  self.c4*self.t4
        
        C[2, 0] =  C[0, 2]
        C[2, 1] =  C[1, 2]
        C[2, 2] =  self.c1*self.lf**2 + self.c2*self.lf**2 + self.c3*self.lr**2 + self.c4*self.lr**2
        C[2, 3] = -self.c1*self.lf
        C[2, 4] = -self.c2*self.lf
        C[2, 5] =  self.c3*self.lr
        C[2, 6] =  self.c4*self.lr
        
        C[3, 0] =  C[0, 3]
        C[3, 1] =  C[1, 3]
        C[3, 2] =  C[2, 3]
        C[3, 3] =  self.c1 + self.cw1
        C[3, 4] =  0.0
        C[3, 5] =  0.0
        C[3, 6] =  0.0
        
        C[4, 0] =  C[0, 4]
        C[4, 1] =  C[1, 4]
        C[4, 2] =  C[2, 4]
        C[4, 3] =  C[3, 4]
        C[4, 4] =  self.c2 + self.cw2
        C[4, 5] =  0.0
        C[4, 6] =  0.0
        
        C[5, 0] =  C[0, 5]
        C[5, 1] =  C[1, 5]
        C[5, 2] =  C[2, 5]
        C[5, 3] =  C[3, 5]
        C[5, 4] =  C[4, 5]
        C[5, 5] =  self.c3 + self.cw3
        C[5, 6] =  0.0
        
        C[6, 0] =  C[0, 6]
        C[6, 1] =  C[1, 6]
        C[6, 2] =  C[2, 6]
        C[6, 3] =  C[3, 6]
        C[6, 4] =  C[4, 6]
        C[6, 5] =  C[5, 6]
        C[6, 6] =  self.c4 + self.cw4
    
        return C
    
    def get_stiffness_matrix(self):
        K = np.zeros([self.number_dofs, self.number_dofs])
        
        K[0, 0] =  self.k1 + self.k2 + self.k3 + self.k4
        K[0, 1] =  self.k1*self.t1 - self.k2*self.t2 + self.k3*self.t3 - self.k4*self.t4
        K[0, 2] =  self.k1*self.lf + self.k2*self.lf - self.k3*self.lr - self.k4*self.lr
        K[0, 3] = -self.k1
        K[0, 4] = -self.k2
        K[0, 5] = -self.k3
        K[0, 6] = -self.k4

        K[1, 0] =  K[0, 1]
        K[1, 1] =  self.k1*self.t1**2 + self.k2*self.t2**2 + self.k3*self.t3**2 + self.k4*self.t4**2
        K[1, 2] =  self.k1*self.t1*self.lf + self.k2*self.t2*self.lf - self.k3*self.t3*self.lr - self.k4*self.t4*self.lr
        K[1, 3] = -self.k1*self.t1
        K[1, 4] =  self.k2*self.t2
        K[1, 5] = -self.k3*self.t3
        K[1, 6] =  self.k4*self.t4

        K[2, 0] =  K[0, 2]
        K[2, 1] =  K[1, 2]
        K[2, 2] =  self.k1*self.lf**2 + self.k2*self.lf**2 + self.k3*self.lr**2 + self.k4*self.lr**2
        K[2, 3] = -self.k1*self.lf
        K[2, 4] = -self.k2*self.lf
        K[2, 5] =  self.k3*self.lr
        K[2, 6] =  self.k4*self.lr

        K[3, 0] =  K[0, 3]
        K[3, 1] =  K[1, 3]
        K[3, 2] =  K[2, 3]
        K[3, 3] =  self.k1 + self.kw1
        K[3, 4] =  0.0
        K[3, 5] =  0.0
        K[3, 6] =  0.0

        K[4, 0] =  K[0, 4]
        K[4, 1] =  K[1, 4]
        K[4, 2] =  K[2, 4]
        K[4, 3] =  K[3, 4]
        K[4, 4] =  self.k2 + self.kw2
        K[4, 5] =  0.0
        K[4, 6] =  0.0

        K[5, 0] =  K[0, 5]
        K[5, 1] =  K[1, 5]
        K[5, 2] =  K[2, 5]
        K[5, 3] =  K[3, 5]
        K[5, 4] =  K[4, 5]
        K[5, 5] =  self.k3 + self.kw3
        K[5, 6] =  0.0

        K[6, 0] =  K[0, 6]
        K[6, 1] =  K[1, 6]
        K[6, 2] =  K[2, 6]
        K[6, 3] =  K[3, 6]
        K[6, 4] =  K[4, 6]
        K[6, 5] =  K[5, 6]
        K[6, 6] =  self.k4 + self.kw4

        return K
    
    def get_F_vector(self, t):
        F = np.zeros(self.number_dofs)
        F[3] = self.wheel_excitation(t)
        F[4] = self.wheel_excitation(t)
        F[5] = self.wheel_excitation(t)
        F[6] = self.wheel_excitation(t)
        return F
        
    def system(self, y, t):
        q, q_dot = np.split(y, 2)
        F = self.get_F_vector(t)
        q_dotdot = np.linalg.solve(self.M, F - np.dot(self.C, q_dot) - np.dot(self.K, q))
        return np.concatenate((q_dot, q_dotdot))
    
    def solve(self):
        solution = scipy.integrate.odeint(self.system, self.initial_conditions, self.time_points)

        self.Zs    = solution[:, 0]
        self.alpha = solution[:, 1]
        self.beta  = solution[:, 2]
        self.Zu1   = solution[:, 3]
        self.Zu2   = solution[:, 4]
        self.Zu3   = solution[:, 5]
        self.Zu4   = solution[:, 6]
        
        self.Zs_dot    = solution[:, 7]
        self.alpha_dot = solution[:, 8]
        self.beta_dot  = solution[:, 9]
        self.Zu1_dot   = solution[:, 10]
        self.Zu2_dot   = solution[:, 11]
        self.Zu3_dot   = solution[:, 12]
        self.Zu4_dot   = solution[:, 13]
        
        return solution
    
    def plot_results(self):
        fig, ax_q = plt.subplots() 
        ax_q.plot(self.time_points, self.Zs,  'k-',   linewidth=2.0, label="Zs")
        ax_q.plot(self.time_points, self.Zu1, 'g-',  linewidth=2.0, label="Zu1")
        ax_q.plot(self.time_points, self.Zu2, 'b--', linewidth=2.0, label="Zu2")
        ax_q.plot(self.time_points, self.Zu3, 'y-',  linewidth=2.0, label="Zu3")
        ax_q.plot(self.time_points, self.Zu4, 'b--', linewidth=2.0, label="Zu4")
        ax_q.grid(color='k', linestyle='-', linewidth=0.3)
        ax_q.set_xlabel('time' )  
        ax_q.set_ylabel('displacement')    
        ax_q.set_title('Displacement')   
        ax_q.legend()
        
        fig, ax_qa = plt.subplots() 
        ax_qa.plot(self.time_points, self.beta,  'r-',   linewidth=2.0, label="theta")
        ax_qa.plot(self.time_points, self.alpha, 'y-',   linewidth=2.0, label="alpha")
        ax_qa.set_xlabel('time' )  
        ax_qa.set_ylabel('angle')    
        ax_qa.set_title('angle')   
        ax_qa.legend()
        
        fig, ax_q_dot = plt.subplots() 
        #ax_q_dot.plot(self.time_points, self.Zs_dot, 'r-', linewidth=2.0, label="Zs_dot")
        ax_q_dot.plot(self.time_points, self.Zu1_dot, 'g-', linewidth=2.0, label="Zu1_dot")
        ax_q_dot.plot(self.time_points, self.Zu2_dot, 'b--', linewidth=2.0, label="Zu2_dot")
        ax_q_dot.plot(self.time_points, self.Zu3_dot, 'g-', linewidth=2.0, label="Zu1_dot")
        ax_q_dot.plot(self.time_points, self.Zu4_dot, 'b--', linewidth=2.0, label="Zu2_dot")
        
        #ax_q_dot.plot(self.time_points[:-1], np.diff(self.Zs)/np.diff(self.time_points), 'k--', linewidth=2.0, label="Zu_dot")
        ax_q_dot.grid(color='k', linestyle='-', linewidth=0.3)
        ax_q_dot.set_xlabel('time' )  
        ax_q_dot.set_ylabel('velocity')    
        ax_q_dot.set_title('Velocity')   
        ax_q_dot.legend()
        plt.show()
