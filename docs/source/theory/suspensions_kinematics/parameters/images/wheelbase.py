import matplotlib.pyplot as plt
import numpy as np

# Create the figure and axes
fig, ax = plt.subplots(figsize=(6, 6))

# Define the rectangle (centered at origin)
rect_points = np.array([[-1, -2],
                        [1, -2],
                        [1, 2],
                        [-1, 2],
                        [-1, -2]])  # Close the rectangle
rotation_angle = np.deg2rad(15)  # 15 degrees tilt

# Rotation matrix for the rectangle
rotation_matrix = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)],
                             [np.sin(rotation_angle),  np.cos(rotation_angle)]])

# Rotate the rectangle
rotated_rect = rect_points @ rotation_matrix.T

# Plot the rotated rectangle
ax.plot(rotated_rect[:, 0], rotated_rect[:, 1], 'k-', linewidth=2)

# Compute and plot the red dashed lines (perpendicular to rectangle's centerline)
center_x = (rotated_rect[0, 0] + rotated_rect[2, 0]) / 2
center_y = (rotated_rect[0, 1] + rotated_rect[2, 1]) / 2

# Line 1 (major diagonal, perpendicular to long side)
perpendicular_angle = rotation_angle + np.pi / 2
line_1_start = [center_x - np.cos(perpendicular_angle) * 2, center_y - np.sin(perpendicular_angle) * 2]
line_1_end = [center_x + np.cos(perpendicular_angle) * 2, center_y + np.sin(perpendicular_angle) * 2]
ax.plot([line_1_start[0], line_1_end[0]], [line_1_start[1], line_1_end[1]], 'r--', linewidth=1.5)

# Line 2 (minor diagonal, perpendicular to short side)
perpendicular_angle_2 = rotation_angle
line_2_start = [center_x - np.cos(perpendicular_angle_2) * 1, center_y - np.sin(perpendicular_angle_2) * 1]
line_2_end = [center_x + np.cos(perpendicular_angle_2) * 1, center_y + np.sin(perpendicular_angle_2) * 1]
ax.plot([line_2_start[0], line_2_end[0]], [line_2_start[1], line_2_end[1]], 'r--', linewidth=1.5)

# Add the reference (horizontal green line)
ax.axhline(0, color='green', linestyle='-', linewidth=1, label="Ref")

# Add vertical dashed lines for Base 1 and Base 2
ax.plot([rotated_rect[0, 0], rotated_rect[0, 0]], [rotated_rect[0, 1], 0], 'k--', linewidth=1)
ax.plot([rotated_rect[2, 0], rotated_rect[2, 0]], [rotated_rect[2, 1], 0], 'k--', linewidth=1)

# Annotate Base 1 and Base 2
ax.text(rotated_rect[0, 0] - 0.2, rotated_rect[0, 1] / 2, 'Base 1', color='black', fontsize=10)
ax.text(rotated_rect[2, 0] + 0.2, rotated_rect[2, 1] / 2, 'Base 2', color='black', fontsize=10)

# Remove axes
ax.axis('off')

# Adjust the plot limits
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

# Show the plot
plt.show()