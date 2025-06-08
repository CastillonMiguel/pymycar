import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle


social = False
# Create the figure and axis
fig, ax = plt.subplots()


car_body = Polygon([[0, 0], [700, -14], [35, 208]], closed=True, color='darkred', edgecolor='black', linestyle='-', linewidth=0.0)
plt.gca().add_artist(car_body)

car_body = Polygon([[307, 117.19], [307, 65], [463.35, 65]], closed=True, color='black', edgecolor='black', linestyle='-', linewidth=0.0)
plt.gca().add_artist(car_body)

car_body = Polygon([[327, 117.19], [327, 80], [476, 80]], closed=True, color='white', edgecolor='black', linestyle='-', linewidth=0.0)
plt.gca().add_artist(car_body)

car_body = Polygon([[25, 169], [129, 119], [15, 131]], closed=True, color='white', edgecolor='black', linestyle='-', linewidth=0.0)
plt.gca().add_artist(car_body)

car_body = Polygon([[-56, 206], [70, 140], [-59, 159]], closed=True, color='black', edgecolor='black', linestyle='-', linewidth=0.0)
plt.gca().add_artist(car_body)

# Draw the wheels
# ===============
rear_wheel = Circle((150, -30), radius=70, color='black', zorder=3)
front_wheel = Circle((546, -30), radius=70, color='black', zorder=3)
plt.gca().add_artist(rear_wheel)
plt.gca().add_artist(front_wheel)

# Add inner white circles to the wheels
rear_wheel = Circle((150, -30), radius=60, color='white', zorder=3)
front_wheel = Circle((546, -30), radius=60, color='white', zorder=3)
plt.gca().add_artist(rear_wheel)
plt.gca().add_artist(front_wheel)


rear_wheel = Circle((150, -30), radius=55, color='black', zorder=3)
front_wheel = Circle((546, -30), radius=55, color='black', zorder=3)
plt.gca().add_artist(rear_wheel)
plt.gca().add_artist(front_wheel)


# Adjust the view
ax.set_xlim(-70, 700)
ax.set_ylim(-120, 210)
# ax.set_aspect('equal', adjustable='box')
# Set aspect ratio to be equal
plt.gca().set_aspect('equal', adjustable='box')
# Remove axes
ax.axis('off')

# Save and show the logo
plt.tight_layout()

if social==False:
    ax.set_xlim(-70, 1500)
    ax.set_ylim(-120, 210)
    plt.text(700, 90, 'pyMyCar', color='black', fontsize=80, va='center', ha='left')
    
if social:
    plt.savefig('logo_social.png', transparent=True)  # Save the plot as an image file
else:
    plt.savefig('logo.png', transparent=True)  # Save the plot as an image file
plt.show()

plt.show()