import math
from typing import List
from vector import Vector


class Matriz:
    """
    Implementación básica de una matriz matemática.

    Esta clase nos ayuda a entender las operaciones matriciales
    fundamentales en Machine Learning.
    """

    def __init__(self, datos: List[List[float]]):
        """
        Inicializa una matriz con una lista de listas.

        Args:
            datos: Lista de filas, donde cada fila es una lista de números
        """
        if not datos or not datos[0]:
            raise ValueError("La matriz debe tener al menos un elemento")

        # Verificar que todas las filas tengan la misma longitud
        longitud_fila = len(datos[0])
        for fila in datos:
            if len(fila) != longitud_fila:
                raise ValueError("Todas las filas deben tener la misma longitud")

        self.datos = datos
        self.filas = len(datos)
        self.columnas = len(datos[0])
        self.forma = (self.filas, self.columnas)

    def __repr__(self):
        """Representación legible de la matriz."""
        filas = []
        for fila in self.datos:
            row_str = " ".join(f"{x:8.3f}" for x in fila)
            filas.append(f"[{row_str}]")
        return f"Matriz(\n  " + "\n  ".join(filas) + "\n)"

    def __getitem__(self, indices):
        """Permite acceso con matriz[i][j] o matriz[i, j]."""
        if isinstance(indices, tuple):
            fila, columna = indices
            return self.datos[fila][columna]
        else:
            return self.datos[indices]

    def __setitem__(self, indices, value):
        """Permite asignación con matriz[i][j] = value."""
        if isinstance(indices, tuple):
            fila, columna = indices
            self.datos[fila][columna] = value
        else:
            fila = indices
            self.datos[fila] = value

    def __add__(self, otra):
        """Suma de matrices (elemento por elemento)."""
        if self.forma != otra.shape:
            raise ValueError("Las matrices deben tener la misma forma")

        datos_resultado = [
            [self.datos[i][j] + otra.datos[i][j] for j in range(self.columnas)]
            for i in range(self.filas)
        ]
        return Matriz(datos_resultado)

    def trasponer(self):
        """
        Calcula la transpuesta de la matriz.

        La transpuesta intercambia filas por columnas.
        Es fundamental en álgebra lineal y en Machine Learning.

        Returns:
            Matriz: Nueva matriz transpuesta
        """
        datos_transpuestos = [
            [self.datos[fila][columna] for fila in range(self.filas)]
            for columna in range(self.columnas)
        ]
        return Matriz(datos_transpuestos)

    def multiplicar_por_escalar(self, escalar):
        """Multiplicación por escalar."""
        datos_resultado = [
            [escalar * self.datos[i][j] for j in range(self.columnas)]
            for i in range(self.filas)
        ]
        return Matriz(datos_resultado)

    def multiplicar_por_vector(self, vector: Vector):
        """
        Multiplica la matriz por un vector.

        Esta es la operación fundamental en redes neuronales:
        cada capa aplica una transformación lineal Ax + b.

        Args:
            vector: Vector a multiplicar

        Returns:
            Vector: Resultado de la multiplicación
        """
        if self.columnas != len(vector):
            raise ValueError(f"Dimensiones incompatibles: matriz {self.forma} * vector {len(vector)}")

        componentes_resultado = []
        for index_fila in range(self.filas):
            fila = [ self.datos[index_fila][columna] for columna in range(self.columnas) ]
            producto_punto = Vector(fila).producto_punto(vector)
            componentes_resultado.append(producto_punto)

        return Vector(componentes_resultado)

    def multiplicar_matrices(self, otra):
        """
        Multiplica dos matrices.

        La multiplicación de matrices permite componer transformaciones.
        En deep learning, representa la composición de capas.

        Args:
            otra: Otra matriz

        Returns:
            Matriz: Resultado de la multiplicación
        """
        if self.columnas != otra.filas:
            raise ValueError(f"Dimensiones incompatibles: {self.forma} * {otra.forma}")

        print(f"   Forma matriz A: {self.forma}")
        print(f"   Forma matriz B: {otra.forma}")

        datos_resultado = []
        for index_fila in range(self.filas):
            fila_i_matriz = [ self.datos[index_fila][columna] for columna in range(self.columnas) ]
            vector_fila_i_matriz = Vector(fila_i_matriz)
            fila_resultado = []
            for index_columna_otra in range(otra.columnas):
                columna_j_matriz_otra = [ otra.datos[fila][index_columna_otra] for fila in range(otra.filas) ]
                vector_columna_j_matriz_otra = Vector(columna_j_matriz_otra)
                fila_resultado.append(vector_fila_i_matriz.producto_punto(vector_columna_j_matriz_otra))
            datos_resultado.append(fila_resultado)

        return Matriz(datos_resultado)

    @staticmethod
    def identidad(tamano: int):
        """
        Crea una matriz identidad de tamaño size * size.

        La matriz identidad es el "1" de las matrices:
        A * I = I * A = A

        Args:
            tamano: Tamaño de la matriz cuadrada

        Returns:
            Matriz: Matriz identidad
        """
        datos = [
            [1.0 if i == j else 0.0 for j in range(tamano)]
            for i in range(tamano)
        ]
        return Matriz(datos)


def rotar_vector(vector: Vector, angulo: int):
    """Rotar vector"""
    angulo_radianes = angulo * math.pi / 180  # angulo en grados convertido a radianes
    matriz_transformacion = Matriz([
        [math.cos(angulo_radianes), -math.sin(angulo_radianes)],
        [math.sin(angulo_radianes),  math.cos(angulo_radianes)]
    ])
    return {
        "matriz_transformacion": matriz_transformacion,
        "vector_rotado": matriz_transformacion.multiplicar_por_vector(vector)
    }

# Ejemplos de uso
def demo_operaciones_matriciales():
    """
    Demuestra las operaciones matriciales con ejemplos de Machine Learning.
    """
    mensaje = "Ejemplos de Operaciones Matriciales"
    print("#" * len(mensaje))
    print(mensaje)
    print("#" * len(mensaje))
    print("\n")

    print("=== Ejemplo 1: Transponer ===")
    datos = Matriz([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0]
    ])
    print(datos)
    print("Transponer...")
    print(datos.trasponer())
    print("\n")

    print("=== Ejemplo 2: Multiplicación matriz por escalar ===")
    print(datos)
    escalar = 3
    print(f"Multiplicación por el escalar: {escalar}...")
    print(datos.multiplicar_por_escalar(escalar))
    print("\n")

    print("=== Ejemplo 3: Multiplicación matriz por vector ===")
    print(datos)
    vector = Vector([1.0, 2.0, 3.0])
    print(f"Multiplicación por el vector: {vector}...")
    print(datos.multiplicar_por_vector(vector))
    print("\n")

    print("=== Ejemplo 4: Multiplicación matriz por matriz ===")
    print(datos)
    otra = Matriz([
        [9.0, 8.0, 7.0],
        [6.0, 5.0, 4.0],
        [3.0, 2.0, 1.0]
    ])
    print(f"Multiplicación por la matriz: {otra}...")
    print(datos.multiplicar_matrices(otra))
    print("\n")

    print("=== Ejemplo 5: Rotación de un vector en 2D ===")
    vector_original = Vector([1.0, 0.0])
    print("\n")

    angulo = 45
    rotacion = rotar_vector(vector_original, angulo)
    print(f"Vector original en 2D: {vector_original}")
    print(f"Matriz de rotacion en {angulo} grados: {rotacion["matriz_transformacion"]}")
    print(f"Vector rotado en {angulo} grados: {rotacion["vector_rotado"]}")
    print("\n")

    angulo = 90
    rotacion = rotar_vector(vector_original, angulo)
    print(f"Vector original en 2D: {vector_original}")
    print(f"Matriz de rotacion en {angulo} grados: {rotacion["matriz_transformacion"]}")
    print(f"Vector rotado en {angulo} grados: {rotacion["vector_rotado"]}")
    print("\n")

    angulo = 180
    rotacion = rotar_vector(vector_original, angulo)
    print(f"Vector original en 2D: {vector_original}")
    print(f"Matriz de rotacion en {angulo} grados: {rotacion["matriz_transformacion"]}")
    print(f"Vector rotado en {angulo} grados: {rotacion["vector_rotado"]}")


if __name__ == "__main__":
    demo_operaciones_matriciales()
