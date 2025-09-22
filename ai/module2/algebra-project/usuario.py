from typing import Dict, List

import numpy as np


class Usuario:
    """
    Clase para representar usuarios en nuestro sistema de recomendaciones.

    Concepto clave: Representación vectorial de usuarios
    ===================================================
    Cada usuario se representa como un vector en un espacio n-dimensional,
    donde n = número de películas. Cada dimensión representa la puntuación
    que el usuario dio a esa película específica.

    Ejemplo: Si tenemos 3 películas [A, B, C] y el usuario puntuó:
    - Película A: 4.5 estrellas
    - Película B: no vista (0.0)
    - Película C: 3.0 estrellas

    El vector del usuario sería: [4.5, 0.0, 3.0]
    """

    def __init__(self, identificacion: str, nombre: str, cantidad_peliculas: int):
        """
        Inicialización del usuario

        Args:
            identificacion: ID único del usuario
            nombre: Nombre del usuario
            cantidad_peliculas: Dimensión del espacio vectorial (número total de películas)

        ¿Por qué usamos NumPy arrays?
          - Operaciones vectoriales eficientes (suma, producto punto, etc.)
          - Aprovecha optimizaciones en C/FORTRAN
          - API consistente para álgebra lineal
        """
        self._id = identificacion
        self._nombre = nombre
        # Vector de puntuaciones inicializado en ceros
        # 0 significa "no visto" o "sin puntuar"
        self._vector_puntuaciones = np.zeros(cantidad_peliculas)

    def actualizar_puntuacion_de_pelicula(self, indice_pelicula: int, puntuacion: float):
        """
        Actualiza la puntuación de una película específica.

        Args:
            indice_pelicula: Índice de la película en el vector de puntuaciones
            puntuacion: Nueva puntuación (típicamente 1.0 - 5.0)

        NOTA IMPORTANTE: Esta es una operación de asignación vectorial.
        Estamos modificando una componente específica del vector usuario.
        """
        self._vector_puntuaciones[indice_pelicula] = puntuacion

    def obtener_id(self) -> str:
        """
        Retorna el ID del usuario.
        """
        return self._id

    def obtener_nombre(self) -> str:
        """
        Retorna el nombre del usuario.
        """
        return self._nombre

    def obtener_vector_puntuaciones(self) -> np.ndarray:
        """
        Retorna el vector de puntuaciones del usuario.

        Returns:
            numpy.ndarray: Vector de puntuaciones del usuario
        """
        return self._vector_puntuaciones.copy()  # Copia para evitar modificaciones accidentales

    def obtener_peliculas_vistas(self) -> List[int]:
        """
        Retorna los índices de las películas que el usuario ha puntuado.

        Returns:
            List[int]: Índices de películas con puntuación > 0
        """
        return [i for i, puntuacion in enumerate(self._vector_puntuaciones) if puntuacion > 0]

    def __str__(self):
        """Representación en texto del usuario."""
        return f"Usuario({self._id}, {self._nombre}, {np.count_nonzero(self._vector_puntuaciones)} películas vistas)"
