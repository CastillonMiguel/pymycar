import matplotlib.pyplot as plt
import numpy as np

# Define the coordinates of the points
Pa = np.array([0, 0])
Pb = np.array([2, 0])
P3 = np.array([3, 1.6])
P4 = np.array([1, 1.2])

# Plot the points
plt.plot(Pa[0], Pa[1], 'ko', label=r'$P_a$')
plt.plot(Pb[0], Pb[1], 'ko', label=r'$P_b$')
plt.plot(P3[0], P3[1], 'ko', label=r'$P_1$')
plt.plot(P4[0], P4[1], 'ko', label=r'$P_2$')

# Plot the bars
plt.plot([Pb[0], P3[0]], [Pb[1], P3[1]], 'k-', label='Bar 2')
plt.plot([P3[0], P4[0]], [P3[1], P4[1]], 'k-', label='Bar 3')
plt.plot([P4[0], Pa[0]], [P4[1], Pa[1]], 'k-', label='Bar 4')

# Annotate the points with coordinates
plt.text(Pa[0], Pa[1], r' $(x_a, y_a)$', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(Pb[0], Pb[1], r' $(x_b, y_b)$', fontsize=12, verticalalignment='bottom', horizontalalignment='left')
plt.text(P3[0], P3[1], r' $(x_1, y_1)$', fontsize=12, verticalalignment='top', horizontalalignment='left')
plt.text(P4[0], P4[1], r' $(x_2, y_2)$', fontsize=12, verticalalignment='top', horizontalalignment='left')

# Add markers to indicate fixed points
plt.plot(Pa[0], Pa[1], 'k^', markersize=10)
plt.plot(Pb[0], Pb[1], 'k^', markersize=10)

# Remove axes
plt.axis('off')

# Set the plot limits
# plt.xlim(-1, 4)
# plt.ylim(-1, 2)

# Add title
# plt.title('4-Bar Mechanism with Natural Coordinates')

# Show the plot
plt.grid(False)
plt.savefig('four_bar_mechanism.png', dpi=300, bbox_inches='tight')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()