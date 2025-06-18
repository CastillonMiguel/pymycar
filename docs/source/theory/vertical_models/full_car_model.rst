.. _theory_full_car_model:

Vertical Car Model
==================

This section presents the full-car vertical dynamics model, which extends the concepts introduced in the half-car model to capture the behavior of all four wheels and the vehicle body. The model consists of a single sprung mass (the vehicle body) and four unsprung masses (one for each wheel assembly), allowing for a comprehensive analysis of ride and handling characteristics.

The system features seven degrees of freedom:
- Vertical displacement of the sprung mass ($Z_s$)
- Roll rotation about the x-axis ($\alpha$)
- Pitch rotation about the y-axis ($\phi$)
- Vertical displacements of each unsprung mass ($Z_{u1}$, $Z_{u2}$, $Z_{u3}$, $Z_{u4}$), corresponding to the front right, front left, rear right, and rear left wheels, respectively.

These degrees of freedom enable the model to represent complex vehicle motions such as heave, pitch, roll, and independent wheel movement. Figure 1 illustrates the arrangement of the masses and the associated coordinates.

.. .. figure:: Coche7GDL.png
..     :scale: 45%
..     :alt: Car Model: 7 Degrees of Freedom
..     :figclass: center

..     Figure 1: Car Model - 7 Degrees of Freedom

The vector of degrees of freedom, denoted as :math:`q`, represents the independent variables that define the configuration of the full car model at any given time. Specifically:

- :math:`Z_s`: Vertical displacement of the car body (sprung mass).
- :math:`\alpha`: Roll angle of the car body.
- :math:`\phi`: Pitch angle of the car body.
- :math:`Z_{u1}`: Vertical displacement of the front right wheel (unsprung mass).
- :math:`Z_{u2}`: Vertical displacement of the front left wheel (unsprung mass).
- :math:`Z_{u3}`: Vertical displacement of the rear right wheel (unsprung mass).
- :math:`Z_{u4}`: Vertical displacement of the rear left wheel (unsprung mass).

Together, these seven variables capture the translational and rotational motion of the car body, as well as the independent vertical motion of each wheel. The time derivatives, :math:`\dot{q}`, represent their respective velocities.

.. math::
   q = (Z_s, \phi, \alpha, Z_{u1}, Z_{u2}, Z_{u3}, Z_{u4})

and

.. math::
   \dot{q} = (\dot{Z_s}, \dot{\phi}, \dot{\alpha}, \dot{Z_{u1}}, \dot{Z_{u2}}, \dot{Z_{u3}}, \dot{Z_{u4}})

.. note::

   The springs and dampers are connected to points $P1$, $P2$, $P3$, and $P4$.


System Parameters for the Car Model
-----------------------------------

The parameters for the complete 7-degree-of-freedom vehicle model are listed in Table 1.

.. table:: Vehicle Parameters - 7 Degrees of Freedom
    :name: t:table7dof
    :class: center

    +------------+-------------------+-----------+----------------+
    | Parameter  | Description       | Parameter  | Description   |
    +============+===================+===========+================+
    | $m_s$      | Sprung Mass       | $l_f$     | Distance CG to |
    |            |                   |           | Front          |
    +------------+-------------------+-----------+----------------+
    | $I_{xx}$   | Roll Inertia      | $l_r$     | Distance CG to |
    |            |                   |           | Rear           |
    +------------+-------------------+-----------+----------------+
    | $I_{yy}$   | Pitch Inertia     | $t_1$     | CG to Front-   |
    |            |                   |           | Right          |
    +------------+-------------------+-----------+----------------+
    | $m_{u1}$   | Unsprung Mass FR  | $t_2$     | CG to Front-   |
    |            |                   |           | Left           |
    +------------+-------------------+-----------+----------------+
    | $m_{u2}$   | Unsprung Mass FL  | $t_3$     | CG to Rear-    |
    |            |                   |           | Right          |
    +------------+-------------------+-----------+----------------+
    | $m_{u3}$   | Unsprung Mass RR  | $t_4$     | CG to Rear-    |
    |            |                   |           | Left           |
    +------------+-------------------+-----------+----------------+
    | $m_{u4}$   | Unsprung Mass RL  | $k_1$     | Suspension     |
    |            |                   |           | Stiffness FR   |
    +------------+-------------------+-----------+----------------+
    | $k_1$      | Suspension        | $k_2$     | Suspension     |
    |            | Stiffness FR      |           | Stiffness FL   |
    +------------+-------------------+-----------+----------------+
    | $k_2$      | Suspension        | $k_3$     | Suspension     |
    |            | Stiffness FL      |           | Stiffness RR   |
    +------------+-------------------+-----------+----------------+
    | $k_3$      | Suspension        | $k_4$     | Suspension     |
    |            | Stiffness RR      |           | Stiffness RL   |
    +------------+-------------------+-----------+----------------+
    | $k_4$      | Suspension        | $k_{w1}$  | Tire Stiffness |
    |            | Stiffness RL      |           | FR             |
    +------------+-------------------+-----------+----------------+
    | $k_{w1}$   | Tire Stiffness FR | $k_{w2}$  | Tire Stiffness |
    |            |                   |           | FL             |
    +------------+-------------------+-----------+----------------+
    | $k_{w2}$   | Tire Stiffness FL | $k_{w3}$  | Tire Stiffness |
    |            |                   |           | RR             |
    +------------+-------------------+-----------+----------------+
    | $k_{w3}$   | Tire Stiffness RR | $k_{w4}$  | Tire Stiffness |
    |            |                   |           | RL             |
    +------------+-------------------+-----------+----------------+

Wheel notations are DD (Front Right), DI (Front Left), TD (Rear Right), and TI (Rear Left).

Energy Calculation:
-------------------

To simplify the calculation of kinetic, dissipated, and potential energy, auxiliary points $P1$, $P2$, $P3$, and $P4$ (represented in green in Figure 1) have been defined. Their coordinates and their derivatives with respect to time, i.e., their velocities, with respect to the vehicle's center of gravity, are detailed below:

.. table:: Coordinates and Velocities of Auxiliary Points
    :class: center

    +-------+------------------------+------------------------+-------------------------------------+
    | Point | $x$                    | $y$                    | $z$                                 |
    +=======+========================+========================+=====================================+
    | $P_1$ | $l_f\cos(\alpha)$      | $t_1\cos(\phi)$        | $z_s+l_f\sin(\alpha)+t_1\sin(\phi)$ |
    +-------+------------------------+------------------------+-------------------------------------+
    | $P_2$ | $l_f\cos(\alpha)$      | $-t_2\cos(\phi)$       | $z_s+l_f\sin(\alpha)-t_2\sin(\phi)$ |
    +-------+------------------------+------------------------+-------------------------------------+
    | $P_3$ | $-l_r\cos(\alpha)$     | $t_3\cos(\phi)$        | $z_s-l_r\sin(\alpha)+t_3\sin(\phi)$ |
    +-------+------------------------+------------------------+-------------------------------------+
    | $P_4$ | $-l_r\cos(\alpha)$     | $-t_4\cos(\phi)$       | $z_s-l_r\sin(\alpha)-t_4\sin(\phi)$ |
    +-------+------------------------+------------------------+-------------------------------------+

    +-------+--------------------------------+-------------------------------+-----------------------------------------------------------------+
    | Point | $\dot{x}$                      | $\dot{y}$                     | $\dot{z}$                                                       |
    +=======+================================+===============================+=================================================================+
    | $P_1$ | $-l_f\sin(\alpha)\dot{\alpha}$ | $-t_1\sin(\phi)\dot{\phi}$    | $\dot{Z_s}+l_f\cos(\alpha)\dot{\alpha}+t_1\cos(\phi)\dot{\phi}$ |
    +-------+--------------------------------+-------------------------------+-----------------------------------------------------------------+
    | $P_2$ | $-l_f\sin(\alpha)\dot{\alpha}$ | $t_2\sin(\phi)\dot{\phi}$     | $\dot{Z_s}+l_f\cos(\alpha)\dot{\alpha}-t_2\cos(\phi)\dot{\phi}$ |
    +-------+--------------------------------+-------------------------------+-----------------------------------------------------------------+
    | $P_3$ | $l_r\sin(\alpha)\dot{\alpha}$  | $-t_3\sin(\phi)\dot{\phi}$    | $\dot{Z_s}-l_r\cos(\alpha)\dot{\alpha}+t_3\cos(\phi)\dot{\phi}$ |
    +-------+--------------------------------+-------------------------------+-----------------------------------------------------------------+
    | $P_4$ | $l_r\sin(\alpha)\dot{\alpha}$  | $t_4\sin(\phi)\dot{\phi}$     | $\dot{Z_s}-l_r\cos(\alpha)\dot{\alpha}-t_4\cos(\phi)\dot{\phi}$ |
    +-------+--------------------------------+-------------------------------+-----------------------------------------------------------------+

.. math::
   \begin{align}
   d_1&=P_{1z}-z_{u1}=z_s+l_f\sin{\alpha}+t_1\sin{\phi}-z_{u1}\\
   d_2&=P_{2z}-z_{u2}=z_s+l_f\sin{\alpha}-t_2\sin{\phi}-z_{u2}\\
   d_3&=P_{1z}-z_{u3}=z_s-l_r\sin{\alpha}+t_3\sin{\phi}-z_{u3}\\
   d_4&=P_{2z}-z_{u4}=z_s-l_r\sin{\alpha}-t_4\sin{\phi}-z_{u4}\\
   v_1&=\dot{P_{1z}}-\dot{z_{u1}}=\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}+t_1\dot{\phi}\cos{\phi}-\dot{z_{u1}}\\
   v_2&=\dot{P_{2z}}-\dot{z_{u2}}=\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}-t_2\dot{\phi}\cos{\phi}-\dot{z_{u2}}\\
   v_3&=\dot{P_{3z}}-\dot{z_{u3}}=\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}+t_3\dot{\phi}\cos{\phi}-\dot{z_{u3}}\\
   v_4&=\dot{P_{4z}}-\dot{z_{u4}}=\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}-t_4\dot{\phi}\cos{\phi}-\dot{z_{u4}}
   \end{align}


Finally, the kinetic energy $T$, dissipated energy $R$, and potential energy $V$ are defined as follows:

Kinetic Energy:
~~~~~~~~~~~~~~~
.. math::
   T = \frac{1}{2}m_s\dot{z_s}^2 + \frac{1}{2}I_{xx}{\dot{\phi}}^2 + \frac{1}{2}I_{yy}{\dot{\alpha}}^2 
       + \frac{1}{2}m_{u1}\ {\dot{z_{u1}}}^2 + \frac{1}{2}m_{u2}\ {\dot{z_{u2}}}^2 
       + \frac{1}{2}m_{u3}\ {\dot{z_{u3}}}^2 + \frac{1}{2}m_{u4}\ {\dot{z_{u4}}}^2

Potential Energy:
~~~~~~~~~~~~~~~~~
.. math::
   V = \frac{1}{2}k_1(d_1)^2 + \frac{1}{2}k_2(d_2)^2 + \frac{1}{2}k_3(d_3)^2 + \frac{1}{2}k_4(d_4)^2 
       + \frac{1}{2}k_{w1}(z_{u1}-z_{01})^2 + \frac{1}{2}k_{w2}(z_{u2}-z_{02})^2 
       + \frac{1}{2}k_{w3}(z_{u3}-z_{03})^2 + \frac{1}{2}k_{w4}(z_{u4}-z_{04})^2

Dissipated Energy:
~~~~~~~~~~~~~~~~~~
.. math::
   R = \frac{1}{2}c_1(v_1)^2 + \frac{1}{2}c_2(v_2)^2 + \frac{1}{2}c_3(v_3)^2 + \frac{1}{2}c_4(v_4)^2 
       + \frac{1}{2}c_{w1}(\dot{z_{u1}}-\dot{z_{01}})^2 + \frac{1}{2}c_{w2}(\dot{z_{u2}}-\dot{z_{02}})^2 
       + \frac{1}{2}c_{w3}(\dot{z_{u3}}-\dot{z_{03}})^2 + \frac{1}{2}c_{w4}(\dot{z_{u4}}-\dot{z_{04}})^2


System Differential Equations
-----------------------------

Applying the Lagrange equation :eq:`lagrange_equation` to the degrees of freedom of the system yields the seven differential equations that define the system:


.. math::
   m_s\ddot{z_s} + c_1({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}+t_1\dot{\phi}\cos{\phi}-\dot{z_{u1}}}) + c_2({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}-t_2\dot{\phi}\cos{\phi}-\dot{z_{u2}}}) + c_3({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}+t_3\dot{\phi}\cos{\phi}-\dot{z_{u3}}}) + c_4({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}-t_4\dot{\phi}\cos{\phi}-\dot{z_{u4}}}) 
   + k_1({z_s+l_f\sin{\alpha}+t_1\sin{\phi}-z_{u1}}) + k_2({z_s+l_f\sin{\alpha}-t_2\sin{\phi}-z_{u2}}) + k_3({z_s-l_r\sin{\alpha}+t_3\sin{\phi}-z_{u3}}) + k_4({z_s-l_r\sin{\alpha}-t_4\sin{\phi}-z_{u4}}) = 0 \\
   I_{xx}\ddot{\phi} + c_1t_1({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}+t_1\dot{\phi}\cos{\phi}-\dot{z_{u1}}}) - c_2t_2({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}-t_2\dot{\phi}\cos{\phi}-\dot{z_{u2}}}) + c_3t_3({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}+t_3\dot{\phi}\cos{\phi}-\dot{z_{u3}}}) - c_4t_4({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}-t_4\dot{\phi}\cos{\phi}-\dot{z_{u4}}}) 
   + k_1t_1({z_s+l_f\sin{\alpha}+t_1\sin{\phi}-z_{u1}}) - k_2t_2({z_s+l_f\sin{\alpha}-t_2\sin{\phi}-z_{u2}}) + k_3t_3({z_s-l_r\sin{\alpha}+t_3\sin{\phi}-z_{u3}}) - k_4t_4({z_s-l_r\sin{\alpha}-t_4\sin{\phi}-z_{u4}}) = 0 \\
   I_{yy}\ddot{\alpha} + c_1l_f({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}+t_1\dot{\phi}\cos{\phi}-\dot{z_{u1}}}) + c_2l_f({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}-t_2\dot{\phi}\cos{\phi}-\dot{z_{u2}}}) - c_3l_r({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}+t_3\dot{\phi}\cos{\phi}-\dot{z_{u3}}}) - c_4l_r({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}-t_4\dot{\phi}\cos{\phi}-\dot{z_{u4}}}) 
   + k_1l_f({z_s+l_f\sin{\alpha}+t_1\sin{\phi}-z_{u1}}) + k_2f_f({z_s+l_f\sin{\alpha}-t_2\sin{\phi}-z_{u2}}) - k_3l_r({z_s-l_r\sin{\alpha}+t_3\sin{\phi}-z_{u3}}) - k_4l_r({z_s-l_r\sin{\alpha}-t_4\sin{\phi}-z_{u4}}) = 0 \\
   m_{u1}\ddot{z_{u1}} - c_1({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}+t_1\dot{\phi}\cos{\phi}-\dot{z_{u1}}}) + c_{w1}(\dot{z_{u1}} - \dot{z_{01}}) - k_1({z_s+l_f\sin{\alpha}+t_1\sin{\phi}-z_{u1}}) + k_{w1}(z_{u1} - z_{01}) = 0 \\
   m_{u2}\ddot{z_{u2}} - c_2({\dot{z_s}+l_f\dot{\alpha}\cos{\alpha}-t_2\dot{\phi}\cos{\phi}-\dot{z_{u2}}}) + c_{w2}(\dot{z_{u2}} - \dot{z_{02}}) - k_2({z_s+l_f\sin{\alpha}-t_2\sin{\phi}-z_{u2}}) + k_{w2}(z_{u2} - z_{02}) = 0 \\
   m_{u3}\ddot{z_{u3}} - c_3({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}+t_3\dot{\phi}\cos{\phi}-\dot{z_{u3}}}) + c_{w3}(\dot{z_{u3}} - \dot{z_{03}}) - k_3({z_s-l_r\sin{\alpha}+t_3\sin{\phi}-z_{u3}}) + k_{w3}(z_{u3} - z_{03}) = 0 \\
   m_{u4}\ddot{z_{u4}} - c_4({\dot{z_s}-l_r\dot{\alpha}\cos{\alpha}-t_4\dot{\phi}\cos{\phi}-\dot{z_{u4}}}) + c_{w4}(\dot{z_{u4}} - \dot{z_{04}}) - k_4({z_s-l_r\sin{\alpha}-t_4\sin{\phi}-z_{u4}}) + k_{w4}(z_{u4} - z_{04}) = 0 \\

Matrix Representation:
----------------------

For small angle variations, we use the approximations $\cos(\theta) \approx 1$ and $\sin(\theta) \approx \theta$. This is because, when $\theta$ is close to zero (measured in radians), the Taylor series expansions of these functions show that higher-order terms become negligible.

.. math::
   [M]{\{\ddot{q}\}} + [C]{\{\dot{q}\}} + [K]{\{q\}} = {F}

Where the matrices are defined as follows:

Mass Matrix [M]:
~~~~~~~~~~~~~~~~
.. math::
   M = \begin{bmatrix}
         m_s & 0 & 0 & 0 & 0 & 0 & 0 \\
         0 & I_{xx} & 0 & 0 & 0 & 0 & 0 \\
         0 & 0 & I_{yy} & 0 & 0 & 0 & 0 \\
         0 & 0 & 0 & m_{u1} & 0 & 0 & 0 \\
         0 & 0 & 0 & 0 & m_{u2} & 0 & 0 \\
         0 & 0 & 0 & 0 & 0 & m_{u3} & 0 \\
         0 & 0 & 0 & 0 & 0 & 0 & m_{u4} \\
       \end{bmatrix}

Stiffness Matrix [K]:
~~~~~~~~~~~~~~~~~~~~~
.. math::
   K = \begin{bmatrix}
         K_{11} & K_{12} & K_{13} & -k_1 & -k_2 & -k_3 & -k_4 \\
         K_{21} & K_{22} & K_{23} & -k_1t_1 & +k_2t_2 & -k_3t_3 & +k_4t_4 \\
         K_{31} & K_{32} & K_{33} & -k_1l_f & -k_2l_f & +k_3l_r & +k_4l_r \\
         -k_1 & -k_1t_1 & -k_1l_f & k_1+k_{w1} & 0 & 0 & 0 \\
         -k_2 & k_2t_2 & -k_2l_f & 0 & k_2+k_{w2} & 0 & 0 \\
         -k_3 & -k_3t_3 & k_3l_r & 0 & 0 & k_3+k_{w3} & 0 \\
         -k_4 & k_4t_4 & k_4l_r & 0 & 0 & 0 & k_4+k_{w4} \\
       \end{bmatrix}

.. math::
   \begin{align*}
      &K_{11}=k_1+k_2+k_3+k_4\\
      &K_{12}=K_{21}=k_1t_1-k_2t_2+k_3t_3-k_4t_4\\
      &K_{13}=K_{31}=k_1l_f+k_2l_f-k_3l_r-k_4l_r\\
      &K_{22}=c_1{t_1}^2+c_2{t_2}^2+k_3{t_3}^2+k_4{t_4}^2\\
      &K_{23}=K_{32}=k_1t_1l_f-k_2t_2l_f-k_3t_3l_r+k_4t_4l_r\\
      &K_{33}=k_1{l_f}^2+k_2{l_f}^2+k_3{l_r}^2+k_4{l_r}^2
   \end{align*}

Damping Matrix [C]:
~~~~~~~~~~~~~~~~~~~
.. math::
   C = \begin{bmatrix}
         C_{11} & C_{12} & C_{13} & -c_1 & -c_2 & -c_3 & -c_4 \\
         C_{21} & C_{22} & C_{23} & -c_1t_1 & +c_2t_2 & -c_3t_3 & +c_4t_4 \\
         C_{31} & C_{32} & C_{33} & -c_1l_f & -c_2l_f & +c_3l_r & +c_4l_r \\
         -c_1 & -c_1t_1 & -c_1l_f & c_1+c_{w1} & 0 & 0 & 0 \\
         -c_2 & c_2t_2 & -c_2l_f & 0 & c_2+c_{w2} & 0 & 0 \\
         -c_3 & -c_3t_3 & c_3l_r & 0 & 0 & c_3+c_{w3} & 0 \\
         -c_4 & c_4t_4 & c_4l_r & 0 & 0 & 0 & c_4+c_{w4} \\
       \end{bmatrix}

.. math::
   \begin{align*}
      &C_{11}=c_1+c_2+c_3+c_4\\
      &C_{12}=C_{21}=c_1t_1-c_2t_2+c_3t_3-c_4t_4\\
      &C_{13}=C_{31}=c_1l_f+c_2l_f-c_3l_r-c_4l_r\\
      &C_{22}=c_1{t_1}^2+c_2{t_2}^2+c_3{t_3}^2+c_4{t_4}^2\\
      &C_{23}=C_{32}=c_1t_1l_f-c_2t_2l_f-c_3t_3l_r+c_4t_4l_r\\
      &C_{33}=c_1{l_f}^2+c_2{l_f}^2+c_3{l_r}^2+c_4{l_r}^2
   \end{align*}

Force Vector {F}:
~~~~~~~~~~~~~~~~~
.. math::
   F = \begin{Bmatrix}
         0 \\
         0 \\
         0 \\
         c_{w1}\dot{z_{01}} + k_{w1}z_{01} \\
         c_{w2}\dot{z_{02}} + k_{w2}z_{02} \\
         c_{w3}\dot{z_{03}} + k_{w3}z_{03} \\
         c_{w4}\dot{z_{04}} + k_{w4}z_{04} \\
       \end{Bmatrix}

Where the vectors and constants are defined as follows:

Vector {q}:
~~~~~~~~~~~
.. math::
   q = \left\{
          \begin{array}{cccc}
            Z_s \\
            \phi \\
            \alpha \\
            Z_{u1} \\
            Z_{u2} \\
            Z_{u3} \\
            Z_{u4}
          \end{array}
        \right\}
