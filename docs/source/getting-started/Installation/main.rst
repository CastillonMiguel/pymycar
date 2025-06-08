Installation manual
===================

Follow these steps to set up your environment:

1. Create a new conda environment:
   
   .. code-block:: sh
   
      conda create -n pymycar-env

2. Activate the new environment:
   
   .. code-block:: sh
   
      conda activate pymycar-env

3. Install FEniCSx, `mpich`, and `pyvista` from the `conda-forge` channel:
   
   .. code-block:: sh
   
      conda install -c conda-forge  pyvista pandas

4. Finally, install the code from this repository:
   
   .. code-block:: sh
   
      pip install pymycar

These steps will set up all the necessary dependencies for running the code in this repository. Make sure to activate the `pymycar-env` environment whenever you work with this project.
