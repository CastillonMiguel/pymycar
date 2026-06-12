import matplotlib.pyplot as plt
import numpy as np

# =========================
# Points
# =========================
P1 = np.array([0.2, 0.5])
P2 = np.array([0.5, 0.5])
P3 = np.array([0.8, 0.5])

# Direction P1 -> P2
direction = P2 - P1
direction = direction / np.linalg.norm(direction)

# =========================
# Figure
# =========================
fig, ax = plt.subplots()

# -------------------------
# P1 and P2 (fixed link)
# -------------------------
ax.plot([P1[0], P2[0]], [P1[1], P2[1]], 'k-', linewidth=2)

ax.plot(P1[0], P1[1], 'ko', markersize=6)
ax.plot(P2[0], P2[1], 'ko', markersize=6)

ax.text(P1[0]-0.02, P1[1]+0.03, "P1", fontsize=12)
ax.text(P2[0]-0.02, P2[1]+0.03, "P2", fontsize=12)

# small "structure hint" under P1-P2 (like your ////)
for i in range(3):
    ax.plot(
        [P1[0] + 0.02*i, P1[0] + 0.02*i + 0.02],
        [P1[1] - 0.08, P1[1] - 0.12],
        'k-', linewidth=1
    )

# -------------------------
# dashed connection to P3
# -------------------------
ax.plot([P2[0], P3[0]], [P2[1], P3[1]], 'k--', linewidth=1)

# -------------------------
# P3
# -------------------------
ax.plot(P3[0], P3[1], 'ko', markersize=6)
ax.text(P3[0]+0.01, P3[1]+0.03, "P3", fontsize=12)

# -------------------------
# motion direction of P3
# -------------------------
# ax.arrow(
#     P3[0], P3[1],
#     -0.15, 0,   # same horizontal direction (constraint idea)
#     head_width=0.02,
#     length_includes_head=True,
#     color='black'
# )

# ax.text(P3[0]-0.1, P3[1]+0.05, "direction", fontsize=10)

# -------------------------
# “mechanism-like” sketch under P2 (//// style)
# -------------------------
for i in range(3):
    ax.plot(
        [P2[0] + 0.02*i, P2[0] + 0.02*i + 0.02],
        [P2[1] - 0.08, P2[1] - 0.12],
        'k-', linewidth=1
    )

# -------------------------
# Clean layout
# -------------------------
ax.set_xlim(0, 1)
ax.set_ylim(0.2, 0.8)
ax.set_aspect('equal')
ax.axis('off')

plt.savefig('aligned_three_point_image.png', dpi=300, bbox_inches='tight')
plt.show()