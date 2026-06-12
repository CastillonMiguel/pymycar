import matplotlib.pyplot as plt
import numpy as np

# Generate some example data for the installation ratio
wheel_displacement = np.linspace(-50, 50, 100)  # Wheel displacement in mm
installation_ratio = 1.0 + 0.01 * wheel_displacement  # Example installation ratio

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the installation ratio
plt.plot(wheel_displacement, installation_ratio, label='Installation Ratio', color='b', linewidth=2)

# Add labels and title
plt.xlabel('Wheel Displacement (mm)')
plt.ylabel('Installation Ratio')
plt.title('Installation Ratio vs. Wheel Displacement')

# Add grid
plt.grid(True)

# Add legend
plt.legend()

# Show the plot
plt.show()