def ver_valores_propios():
    """
    Visualiza conceptualmente los valores y los vectores propios.
    Esta es una simplificación para matrices 2x2.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Matriz de ejemplo
    A = np.array([[3, 1], [0, 2]])

    # Calcular valores y vectores propios usando NumPy
    valores_propios, vectores_propios = np.linalg.eig(A)

    # Crear varios vectores para mostrar la transformación
    angles = np.linspace(0, 2*np.pi, 16)
    vectores_originales = np.array([[np.cos(a), np.sin(a)] for a in angles])
    vectores_transformados = np.array([A @ v for v in vectores_originales])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Vectores originales
    ax1.set_aspect('equal')
    for v in vectores_originales:
        ax1.arrow(0, 0, v[0], v[1], head_width=0.05, head_length=0.1,
                 fc='blue', ec='blue', alpha=0.6)

    # Vectores propios originales
    for i, (val, vec) in enumerate(zip(valores_propios, vectores_propios.T)):
        ax1.arrow(0, 0, vec[0], vec[1], head_width=0.1, head_length=0.15,
                 fc='red', ec='red', linewidth=3,
                 label=f'Vector propio {i+1}')

    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_title('Vectores Originales')
    ax1.grid(True)
    ax1.legend()

    # Vectores transformados
    ax2.set_aspect('equal')
    for v in vectores_transformados:
        ax2.arrow(0, 0, v[0], v[1], head_width=0.05, head_length=0.1,
                 fc='green', ec='green', alpha=0.6)

    # Vectores propios transformados (escalados por valor propio)
    for i, (val, vec) in enumerate(zip(valores_propios, vectores_propios.T)):
        vectores_propios_transformados = val * vec
        ax2.arrow(0, 0, vectores_propios_transformados[0], vectores_propios_transformados[1],
                 head_width=0.1, head_length=0.15, fc='red', ec='red',
                 linewidth=3, label=f'λ{i+1}={val:.1f} × eigenvec{i+1}')

    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_title('Vectores Transformados por A')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()

    print(f"Valores propios: {valores_propios}")
    print(f"Vectores propios:\n{vectores_propios}")


ver_valores_propios()
