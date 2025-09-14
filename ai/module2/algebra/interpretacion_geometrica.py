import matplotlib.pyplot as plt
import numpy as np


def dibujar_vector(vector, color='blue', label='Vector'):
    plt.quiver(0, 0, vector[0], vector[1],
               angles='xy', scale_units='xy', scale=1,
               color=color, label=label, width=0.005)
    plt.xlim(-1, 5)
    plt.ylim(-1, 5)
    plt.grid(True)
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)


# Ejemplo: vector que representa preferencias de usuario
preferencias_usuario = np.array([3, 4])  # [acción: 3, comedia: 4]
plt.figure(figsize=(8, 6))
dibujar_vector(preferencias_usuario, 'blue', 'Preferencias Usuario')
plt.xlabel('Rating Acción')
plt.ylabel('Rating Comedia')
plt.title('Vector de Preferencias de Usuario')
plt.legend()
plt.show()
