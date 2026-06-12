import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, ax = plt.subplots()

# Define the points
x_points = [0.1, 0.7, 0.6]
y_points = [0.3, 0.2, 0.7]

# Plot the points
ax.plot(x_points[0], y_points[0], 'o')  # Point 1
ax.plot(x_points[1], y_points[1], 'o')  # Point 2
ax.plot(x_points[2], y_points[2], 'o')  # Point 3

# Add labels to the points
ax.text(x_points[0]-0.05, y_points[0], '1', fontsize=12)
ax.text(x_points[1]+0.02, y_points[1], '3', fontsize=12)
ax.text(x_points[2]-0.03, y_points[2]+0.02, '2', fontsize=12)

# Draw dashed lines connecting the points
ax.plot([x_points[0], x_points[2]], [y_points[0], y_points[2]], 'k--')  # L12
ax.plot([x_points[2], x_points[1]], [y_points[2], y_points[1]], 'k--')  # L23
ax.plot([x_points[0], x_points[1]], [y_points[0], y_points[1]], 'k--')  # L13

# Label the lines with increased distance from the lines
ax.text((x_points[0] + x_points[2]) / 2 - 0.07, (y_points[0] + y_points[2]) / 2 + 0.05, '$L_{12}$', fontsize=12)
ax.text((x_points[2] + x_points[1]) / 2 + 0.05, (y_points[2] + y_points[1]) / 2, '$L_{23}$', fontsize=12)
ax.text((x_points[0] + x_points[1]) / 2, (y_points[0] + y_points[1]) / 2 - 0.06, '$L_{13}$', fontsize=12)


# Create an irregular closed curve around the points
theta = np.linspace(0, 2 * np.pi, 100)
r = 0.5 + 0.1 * np.sin(4 * theta)  # Irregular radius
x_boundary = 0.5 + r * np.cos(theta)
y_boundary = 0.5 + r * np.sin(theta)
ax.plot(x_boundary, y_boundary, 'k-')

# Adjust axis limits and remove axes
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)
ax.axis('off')

# Save the plot to a file
plt.savefig('solid_3_points.png', dpi=300, bbox_inches='tight')
plt.show()