.. _theory_half_car_model:

Half car model
==============

The half car model is a simplified representation of a vehicle's dynamics that can be formulated to analyze either longitudinal (front-to-rear) or transversal (side-to-side) motions. In the longitudinal case, it focuses on vertical and pitch dynamics, while in the transversal case, it can be adapted to study vertical and roll dynamics. By selecting the appropriate orientation, the model provides insight into either the vehicle's response to bumps and braking (longitudinal dynamics) or its behavior during cornering and lateral load transfer (transversal dynamics).

The model consists of a single sprung mass (the vehicle body) and two unsprung masses (representing the wheels and their assemblies at either the front and rear, or left and right, depending on the chosen direction). It captures four degrees of freedom: the vertical displacement of the vehicle body ($Z_s$), its pitch or roll rotation ($\theta$), and the vertical displacements of the two unsprung masses ($Z_{u1}$ and $Z_{u2}$). These degrees of freedom allow the model to describe both the heave (up-and-down motion) and pitch or roll (tilting) of the vehicle, as well as the independent vertical motions of the wheels.

This flexibility makes the half car model a valuable tool for investigating a range of vehicle dynamic behaviors, offering a balance between physical realism and computational simplicity compared to the quarter car model.

.. code-block::
                                              
    #     -----------------------------------/ ------------------------------
    #     |                           ^     /  theta                         |
    #  p1 *            ms Is      zs _|_   *- - -                            * p2
    #     |                                                                  |
    #     --------------------------------------------------------------------
    #           \       |                                     \       |
    #       k1  /      |_| c1                             k2  /      |_| c2
    #           \       |                                     \       |
    #        ---------------       ^                       ---------------       ^
    #        |             |       | zu2                   |             |       | zu2
    #        |     mu1     |      ---                      |     mu2     |      ---
    #        |             |                               |             |   
    #        ---------------                               ---------------
    #           \       |                                     \       |
    #       kw1 /      |_| cw1                            kw2 /      |_| cw2
    #           \       |                                     \       |
    #           ---------                                     ---------
    #             \   /                                         \   /
    #               *    __      __     ^                         *    __      __     ^    
    #       ____________/  \    /  \__  | z01             ____________/  \    /  \__  | z02
    #                       \__/                                          \__/                  


The vector of degrees of freedom, denoted as :math:`q`, represents the independent variables that define the configuration of the half car model at any given time. Specifically:

- :math:`Z_s`: Vertical displacement of the car body (sprung mass).
- :math:`\theta`: Pitch angle of the car body.
- :math:`Z_{u1}`: Vertical displacement of the front wheel (unsprung mass).
- :math:`Z_{u2}`: Vertical displacement of the rear wheel (unsprung mass).

Together, these four variables capture both the translational and rotational motion of the car body, as well as the vertical motion of each wheel. The time derivatives, :math:`\dot{q}`, represent their respective velocities.

.. math::
    q = (Z_s, \theta, Z_{u1}, Z_{u2})

and 

.. math::
    \dot{q} = (\dot{Z_s}, \dot{\theta}, \dot{Z_{u1}}, \dot{Z_{u2}})

.. note:: 
   
   The springs and dampers are connected to points $P1$ and $P2$.


System Parameters for the Half Car Model
----------------------------------------

.. table:: Vehicle Parameters - Half Car Model
    :name: t:tabl2HalfCarModeldof
    :class: center

    +----------------------------+-------------------+
    | **Parameters: Half Car**   |                   |
    | **Model: 4 Degrees of      |                   |
    | Freedom**                  |                   |
    +----------------------------+-------------------+
    | $m_s$                      | Sprung Mass       |
    +----------------------------+-------------------+
    | $I_s$                      | Inertia           |
    +----------------------------+-------------------+
    | $m_{u1}$                   | Unsprung Mass 1   |
    +----------------------------+-------------------+
    | $m_{u2}$                   | Unsprung Mass 2   |
    +----------------------------+-------------------+
    | $k_1$                      | Suspension        |
    |                            | Stiffness 1       |
    +----------------------------+-------------------+
    | $k_2$                      | Suspension        |
    |                            | Stiffness 2       |
    +----------------------------+-------------------+
    | $c_1$                      | Suspension        |
    |                            | Damping 1         |
    +----------------------------+-------------------+
    | $c_2$                      | Suspension        |
    |                            | Damping 2         |
    +----------------------------+-------------------+
    | $k_{w1}$                   | Tire Stiffness 1  |
    +----------------------------+-------------------+
    | $k_{w2}$                   | Tire Stiffness 2  |
    +----------------------------+-------------------+
    | $c_{w1}$                   | Tire Damping 1    |
    +----------------------------+-------------------+
    | $c_{w2}$                   | Tire Damping 2    |
    +----------------------------+-------------------+
    | $l_1$                      | CG Distance to P1 |
    +----------------------------+-------------------+
    | $l_2$                      | CG Distance to P2 |
    +----------------------------+-------------------+


Energy Calculation:
-------------------

To simplify the calculation of kinetic, dissipated, and potential energy, auxiliary points $P1$ and $P2$ have been defined. Their coordinates, as well as their time derivatives (i.e., velocities) with respect to the center of gravity of the vehicle, are detailed below:

.. table::

    +---------+---------------------+------------------------+--------------------------------+-----------------------------------------+
    | Point   | $y$                 | $z$                    | $\dot{y}$                      | $\dot{z}$                               |
    +---------+---------------------+------------------------+--------------------------------+-----------------------------------------+
    | $P_1$   | $-l_1\cos(\theta)$  | $z_s-l_1\sin(\theta)$  | $l_1\sin(\theta)\dot{\theta}$  | $\dot{z_s}-l_1\cos(\theta)\dot{\theta}$ |
    +---------+---------------------+------------------------+--------------------------------+-----------------------------------------+
    | $P_2$   | $l_2\cos(\theta)$   | $z_s+l_2\sin(\theta)$  | $-l_2\sin(\theta)\dot{\theta}$ | $\dot{z_s}+l_2\cos(\theta)\dot{\theta}$ |
    +---------+---------------------+------------------------+--------------------------------+-----------------------------------------+

This introduces the following terms, representing the relative distances ($d_1$ and $d_2$) from points $P1$ and $P2$ to the respective unsprung masses $m_{u1}$ and $m_{u2}$, as well as the velocities ($v_1$ and $v_2$):

.. math::
   d_1 &= P_{1z} - z_{u1} = z_s - l_1\sin{\theta} - z_{u1} \\
   d_2 &= P_{2z} - z_{u2} = z_s + l_2\sin{\theta} - z_{u2} \\
   v_1 &= \dot{P_{1z}} - \dot{z_{u1}} = \dot{z_s} - l_1\dot{\theta}\cos{\theta} - \dot{z_{u1}} \\
   v_2 &= \dot{P_{2z}} - \dot{z_{u2}} = \dot{z_s} + l_2\dot{\theta}\cos{\theta} - \dot{z_{u2}}

It's important to note that only vertical direction actions of springs and dampers are considered.

* Kinetic energy $T$
.. math::
   T = \frac{1}{2}m_s{\dot{z_s}}^2 + \frac{1}{2}I_s{\dot{\theta}}^2 + \frac{1}{2}m_{u1}{\dot{z_{u1}}}^2 + \frac{1}{2}m_{u2}{\dot{z_{u2}}}^2 

* Dissipated energy $R$
.. math::
   V = \frac{1}{2}k_1(d_1)^2 + \frac{1}{2}k_2(d_2)^2 + \frac{1}{2}k_{w1}(z_{u1}-z_{01})^2 + \frac{1}{2}k_{w2}(z_{u2}-z_{02})^2 

* Potential energy $V$ 
.. math::
   R = \frac{1}{2}c_1(v_1)^2 + \frac{1}{2}c_2(v_2)^2 + \frac{1}{2}c_{w1}(\dot{z_{u1}}-\dot{z_{01}})^2 + \frac{1}{2}c_{w2}(\dot{z_{u2}}-\dot{z_{02}})^2

Applying the Lagrange equation :eq:`lagrange_equation` to the degrees of freedom of the system results in the following four differential equations that define the system:

.. math::

   m_s\ddot{z_s} &+ c_1({\dot{z_s}-l_1\dot{\theta}\cos{\theta}-\dot{z_{u1}}}) + c_2({\dot{z_s}+l_2\dot{\theta}\cos{\theta}-\dot{z_{u2}}}) + k_1({z_s-l_1\sin{\theta}-z_{u1}}) + k_2({z_s+l_2\sin{\theta}-z_{u2}}) = 0 \\
   I_s\ddot{\theta} &- c_1l_1({\dot{z_s}-l_1\dot{\theta}\cos{\theta}-\dot{z_{u1}}}) + c_2l_2({\dot{z_s}+l_2\dot{\theta}\cos{\theta}-\dot{z_{u2}}}) - k_1l_1({z_s-l_1\sin{\theta}-z_{u1}}) + k_2l_2({z_s+l_2\sin{\theta}-z_{u2}}) = 0 \\
   m_{u1}\ddot{z_{u1}} &- c_1({\dot{z_s}-l_1\dot{\theta}\cos{\theta}-\dot{z_{u1}}}) + c_{w1}(\dot{z_{u1}}-\dot{z_{01}}) - k_1({z_s-l_1\sin{\theta}-z_{u1}}) + k_{w1}(z_{u1}-z_{01}) = 0 \\
   m_{u2}\ddot{z_{u2}} &- c_2({\dot{z_s}+l_2\dot{\theta}\cos{\theta}-\dot{z_{u2}}}) + c_{w2}(\dot{z_{u2}}-\dot{z_{02}}) - k_2({z_s+l_2\sin{\theta}-z_{u2}}) + k_{w2}(z_{u2}-z_{02}) = 0


Matrix Representation:
----------------------

For small angle variations, we use the approximations $\cos(\theta) \approx 1$ and $\sin(\theta) \approx \theta$. This is because, when $\theta$ is close to zero (measured in radians), the Taylor series expansions of these functions show that higher-order terms become negligible.

.. math::
   [M]{\{\ddot{q}\}} + [C]{\{\dot{q}\}} + [K]{\{q\}} = {F}

.. math::
   M = \begin{bmatrix}
            m_s & 0 & 0 & 0 \\
            0 & I_s & 0 & 0 \\
            0 & 0 & m_{u1} & 0 \\
            0 & 0 & 0 & m_{u2}
        \end{bmatrix}

.. math::
   C = \begin{bmatrix}
            c_1+c_2 & -c_1l_1+c_2l_2 & -c_1 & -c_2 \\
            -c_1l_1+c_2l_2 & c_1{l_1}^2+c_2{l_2}^2 & c_1l_1 & -c_2l_2 \\
            -c_1 & c_1l_1 & c_1+c_{w1} & 0 \\
            -c_2 & -c_2l_2 & 0 & c_2+c_{w2}
        \end{bmatrix}

.. math::
   K = \begin{bmatrix}
            k_1+k_2 & -k_1l_1+k_2l_2 & -k_1 & -k_2 \\
            -k_1l_1+k_2l_2 & k_1{l_1}^2+k_2{l_2}^2 & k_1l_1 & -k_2l_2 \\
            -k_1 & k_1l_1 & k_1+k_{w1} & 0 \\
            -k_2 & -k_2l_2 & 0 & k_2+k_{w2}
        \end{bmatrix}

.. math::
   F = \begin{Bmatrix}
            0 \\
            0 \\
            c_{w1}\dot{z_{01}}+k_{w1}z_{01} \\
            c_{w2}\dot{z_{02}}+k_{w2}z_{02}
        \end{Bmatrix}
        