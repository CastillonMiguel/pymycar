import matplotlib.pyplot as plt
import numpy as np

# Create the figure and axes
fig, ax = plt.subplots(figsize=(6, 6))

# Draw the circle
circle = plt.Circle((0, 0), radius=1, color='gray', ec='black', linewidth=2, alpha=0.5)
ax.add_artist(circle)

# Plot the ground line
ax.plot([-2, 2], [-1, -1], 'k-', linewidth=2)  # Ground line

# Plot the vertical red dashed line (z-axis through the circle center)
ax.plot([0, 0], [-1, 1.5], 'r--', linewidth=1.5)

# Plot the horizontal red dashed line (centerline of the circle)
ax.plot([-1, 1], [0, 0], 'r--', linewidth=1.5)

# Add the tilted yellow dashed line
tilt_angle = np.deg2rad(15)  # Tilt angle (tau) in radians
aux = -0.85
aux2 = 0.5
tilt_line_x = [aux, aux2]
tilt_line_y = [-1.0, 1.5]
ax.plot(tilt_line_x, tilt_line_y, color='orange', linestyle='--', linewidth=1.5)

tilt_line_x2 = [aux, aux]
tilt_line_y2 = [-1.0,  -1.2]
ax.plot(tilt_line_x2, tilt_line_y2, color='black', linestyle='-', linewidth=1.5)

tilt_line_x2 = [0.0, 0.0]
tilt_line_y2 = [-1.0,  -1.2]
ax.plot(tilt_line_x2, tilt_line_y2, color='black', linestyle='-', linewidth=1.5)

# Add the caster trail (distance between z-axis and yellow line intersection with the ground)
caster_trail_length = np.tan(tilt_angle)  # Length of caster trail on the ground
ax.plot([-aux, 0], [-1, -1], 'k--', linewidth=1)

# Annotate the caster trail
# ax.annotate("", xy=(-0.4, -1.2), xytext=(0, 0),
#             arrowprops=dict(arrowstyle="->"))
ax.arrow(aux, -1.2, -aux, 0)
# ax.annotate('Caster Trail',
#             xy=(-0.85, -1.4), 
#             ha='center', color='black', fontsize=10,
#             arrowprops=dict(arrowstyle='|-|', color='black'))

# Add angle annotation (tau)
arc_radius = 1.2
arc_x = [arc_radius * np.sin(a) for a in np.linspace(np.deg2rad(0), tilt_angle, 100)]
arc_y = [arc_radius * np.cos(a) for a in np.linspace(np.deg2rad(0), tilt_angle, 100)]
ax.plot(arc_x, arc_y, 'k-', linewidth=1)
ax.text(0.2, 1.3, r'$\tau$', fontsize=12)

# Add coordinate axes
# ax.quiver(0, 0, 1.5, 0, angles='xy', scale_units='xy', scale=1, color='black', label='X')  # X-axis
# ax.quiver(0, 0, 0, 1.5, angles='xy', scale_units='xy', scale=1, color='black', label='Z')  # Z-axis

# Set limits and aspect ratio
ax.set_xlim(-2, 2)
ax.set_ylim(-1.5, 2)
ax.set_aspect('equal', adjustable='box')

# Remove axes
ax.axis('off')

# Show the plot
plt.show()