import numpy as np
import matplotlib.pyplot as plt


def derivada_numerica(func, x, h=1e-7):
    """
    Calcula la derivada numérica usando la definición de límite
    """
    return (func(x + h) - func(x)) / h


def comparar_derivadas():
    """
    Compara derivadas numéricas vs analíticas
    """
    # Función test: f(x) = x³ + 2x² - 5x + 1
    def f(x):
        return x**3 + 2*x**2 - 5*x + 1

    def f_derivada_analitica(x):
        # f'(x) = 3x² + 4x - 5
        return 3*x**2 + 4*x - 5

    puntos = np.linspace(-3, 3, 10)

    print("Comparación Derivadas Numéricas vs Analíticas:")
    print("-" * 60)
    print(f"{'x':>8} {'Numérica':>12} {'Analítica':>12} {'Error':>12}")
    print("-" * 60)

    for x in puntos:
        numerica = derivada_numerica(f, x)
        analitica = f_derivada_analitica(x)
        error = abs(numerica - analitica)

        print(f"{x:>8.2f} {numerica:>12.6f} {analitica:>12.6f} {error:>12.2e}")

    # Visualización
    x_plot = np.linspace(-3, 3, 1000)
    y_original = [f(x) for x in x_plot]
    y_derivada_num = [derivada_numerica(f, x) for x in x_plot]
    y_derivada_ana = [f_derivada_analitica(x) for x in x_plot]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    ax1.plot(x_plot, y_original, 'b-', linewidth=2,
             label='f(x) = x³ + 2x² - 5x + 1')
    ax1.set_title('Función Original')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(x_plot, y_derivada_ana, 'g-', linewidth=2,
             label="Analítica: f'(x) = 3x² + 4x - 5")
    ax2.plot(x_plot, y_derivada_num, 'r--',
             linewidth=2, alpha=0.7, label='Numérica')
    ax2.set_title('Comparación de Derivadas')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


comparar_derivadas()
