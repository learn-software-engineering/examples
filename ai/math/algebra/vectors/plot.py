import matplotlib.pyplot as plt

v = [3, 2]

plt.figure(figsize=(6,6))

# Flecha del vector
plt.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color='blue')

# Punto final
plt.scatter(v[0], v[1], color='red')
plt.text(v[0] + 0.1, v[1] + 0.1, "(3, 2)", fontsize=12)

# Texto indicando qué es la flecha
plt.text(v[0] * 0.6, v[1] * 0.5, "vector v = [3, 2]", fontsize=12, color='blue')

# Ejes
plt.xlim(0, 4)
plt.ylim(0, 3)
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
