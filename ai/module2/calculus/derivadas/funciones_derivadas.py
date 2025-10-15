import numpy as np
import matplotlib.pyplot as plt


def mostrar_funciones_y_derivadas():
    """
    Visualización de funciones comunes y sus derivadas
    """
    x = np.linspace(-5, 5, 1000)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()

    # 1. Función cuadrática
    y1 = x**2
    dy1 = 2*x
    axes[0].plot(x, y1, 'b-', label='f(x) = x²', linewidth=2)
    axes[0].plot(x, dy1, 'r--', label="f'(x) = 2x", linewidth=2)
    axes[0].set_title('Función Cuadrática')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 2. Función exponencial
    y2 = np.exp(x)
    dy2 = np.exp(x)  # Su propia derivada!
    axes[1].plot(x, y2, 'b-', label='f(x) = eˣ', linewidth=2)
    axes[1].plot(x, dy2, 'r--', label="f'(x) = eˣ", linewidth=2)
    axes[1].set_title('Función Exponencial')
    axes[1].set_ylim(0, 10)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # 3. Función sigmoid (súper importante en ML)
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivada(x):
        s = sigmoid(x)
        return s * (1 - s)

    y3 = sigmoid(x)
    dy3 = sigmoid_derivada(x)
    axes[2].plot(x, y3, 'b-', label='σ(x) = 1/(1+e⁻ˣ)', linewidth=2)
    axes[2].plot(x, dy3, 'r--', label="σ'(x) = σ(x)(1-σ(x))", linewidth=2)
    axes[2].set_title('Función Sigmoid (Activación Neural)')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    # 4. Función logarítmica
    x_pos = x[x > 0.1]  # Evitar log de números negativos
    y4 = np.log(x_pos)
    dy4 = 1/x_pos
    axes[3].plot(x_pos, y4, 'b-', label='f(x) = ln(x)', linewidth=2)
    axes[3].plot(x_pos, dy4, 'r--', label="f'(x) = 1/x", linewidth=2)
    axes[3].set_title('Función Logarítmica')
    axes[3].set_xlim(0.1, 5)
    axes[3].legend()
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

mostrar_funciones_y_derivadas()
