import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, ax = plt.subplots()

# Define the points
x_points = [0.3, 0.7]
y_points = [0.5, 0.5]

# Plot the points
ax.plot(x_points[0], y_points[0], 'o', label='Point 1')  # Point 1
ax.plot(x_points[1], y_points[1], 'o', label='Point 2')  # Point 2

# Add labels to the points
ax.text(x_points[0]-0.05, y_points[0], '1', fontsize=12)
ax.text(x_points[1]+0.02, y_points[1], '2', fontsize=12)

# Draw a dashed line connecting the two points
ax.plot(x_points, y_points, 'k--', label='Dashed Line')

# Label the line
ax.text((x_points[0] + x_points[1]) / 2, y_points[0] + 0.02, '$L_{12}$', fontsize=12)

# Create an irregular closed curve around the points
theta = np.linspace(0, 2 * np.pi, 100)
r = 0.5 + 0.1 * np.sin(4 * theta)  # Irregular radius
x_boundary = 0.5 + r * np.cos(theta)
y_boundary = 0.5 + r * np.sin(theta)
ax.plot(x_boundary, y_boundary, 'k-', label='Boundary')

# Adjust axis limits and remove axes
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)
ax.axis('off')

# Display the plot
plt.savefig('solid_2_points.png', dpi=300, bbox_inches='tight')
plt.show()