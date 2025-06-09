"""
Animation
=========
"""

import pyvista as pv
import os

def create_animation(data, solution, name="movie"):
    """
    Create and save an animation of the suspension or chassis movement.

    Parameters
    ----------
    data : object
        The data object containing geometry and state information for the animation.
        This object should provide methods such as `set_frame` and `add_mesh`.
    solution : object
        The solution object containing the results or states to animate.
    name : str, optional
        The base name for the output movie file (default is "movie").

    Notes
    -----
    - The function expects the `data` object to have `uca_outer`, `set_frame`, and `add_mesh` attributes/methods.
    - The animation is saved as an MP4 file in the current working directory.
    - The frame rate is set so that the animation lasts approximately 5 seconds.
    - The function uses PyVista for 3D visualization and animation.
    """
    total_frames = len(self.uca_outer)
    fps = total_frames / 5

    plotter = pv.Plotter()
    # plotter.camera_position = 'xz'
    plotter = pv.Plotter(off_screen=False)

    plotter.open_movie(os.path.join(name, '.mp4'), framerate=fps, quality=5)

    # self.set_frame(0)
    self.add_mesh(plotter)
    # plotter.show()

    # Add initial mesh to setup the camera
    plotter.background_color = 'w'

    # Run through each frame
    plotter.write_frame()  # write initial data

    # clear and overwrite the mesh on each frame
    for i in range(total_frames):
        self.set_frame(i)
        self.add_mesh(plotter)
        plotter.write_frame()  # Write this frame
        plotter.clear()

        _ = plotter.add_text(f"Time: {i:.0f}", color="black")
        plotter.enable_lightkit()
        # time.sleep(1/fps)

    # Be sure to close the plotter when finished
    plotter.close()
