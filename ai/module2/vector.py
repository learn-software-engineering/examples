import math
from typing import List


class Vector:
    """
    Implementación básica de un vector matemático.

    Esta clase nos ayuda a entender las operaciones vectoriales
    antes de usar bibliotecas optimizadas como NumPy.
    """

    def __init__(self, componentes: List[float]):
        """
        Inicializa un vector con una lista de componentes.

        Args:
            componentes: Lista de números que forman el vector
        """
        if not componentes:
            raise ValueError("Un vector debe tener al menos un componente")
        self.componentes = componentes
        self.dimension = len(componentes)

    def __repr__(self):
        return f"Vector({self.componentes})"

    def __len__(self):
        return self.dimension

    def __getitem__(self, index):
        return self.componentes[index]

    def __add__(self, otro_vector):
        """
        Suma vectorial: componente por componente.

        Ejemplo:
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        v3 = v1 + v2  # Vector([5, 7, 9])
        """
        if self.dimension != otro_vector.dimension:
            raise ValueError("Los vectores deben tener la misma dimensión")

        componentes_resultado = [
            a + b for a, b in zip(self.componentes, otro_vector.componentes)
        ]
        return Vector(componentes_resultado)

    def __sub__(self, otro_vector):
        """Resta vectorial."""
        if self.dimension != otro_vector.dimension:
            raise ValueError("Los vectores deben tener la misma dimensión")

        componentes_resultado = [
            a - b for a, b in zip(self.componentes, otro_vector.componentes)
        ]
        return Vector(componentes_resultado)

    def __mul__(self, escalar):
        """
        Multiplicación por escalar.

        Ejemplo:
        v = Vector([1, 2, 3])
        v_scaled = v * 2  # Vector([2, 4, 6])
        """
        return Vector([escalar * componente for componente in self.componentes])

    def producto_punto(self, otro_vector):
        """
        Producto punto: la operación más importante en Machine Learning.

        El producto punto mide la similitud direccional entre vectores.
        - Producto alto: vectores apuntan en direcciones similares
        - Producto cero: vectores perpendiculares
        - Producto negativo: vectores apuntan en direcciones opuestas

        Args:
            otro_vector: Otro vector de la misma dimensión

        Returns:
            float: El producto punto
        """
        if self.dimension != otro_vector.dimension:
            raise ValueError("Los vectores deben tener la misma dimensión")

        return sum(a * b for a, b in zip(self.componentes, otro_vector.componentes))

    def magnitud(self):
        """
        Calcula la magnitud (norma) del vector.

        La magnitud representa la "longitud" del vector.
        Es importante para normalización y cálculo de distancias.

        Returns:
            float: La magnitud del vector
        """
        return math.sqrt(sum(componente ** 2 for componente in self.componentes))

    def normalizar(self):
        """
        Normaliza el vector (magnitud = 1).

        Los vectores normalizados son cruciales en Machine Learning porque:
        - Eliminan el efecto de la escala
        - Facilitan la comparación de direcciones
        - Son requeridos en muchos algoritmos

        Returns:
            Vector: Nuevo vector normalizado
        """
        mag = self.magnitud()
        if mag == 0:
            raise ValueError("No se puede normalizar el vector cero")

        return Vector([componente / mag for componente in self.componentes])

    def similitud_coseno(self, otro_vector):
        """
        Calcula la similitud coseno entre dos vectores.

        La similitud coseno es fundamental en:
        - Sistemas de recomendación
        - Procesamiento de lenguaje natural
        - Búsqueda semántica

        Retorna valores entre -1 y 1:
        - 1: Vectores idénticos en dirección
        - 0: Vectores perpendiculares
        - -1: Vectores opuestos

        Args:
            otro_vector: Otro vector

        Returns:
            float: Similitud coseno
        """
        dot_prod = self.producto_punto(otro_vector)
        producto_magnitudes = self.magnitud() * otro_vector.magnitud()

        if producto_magnitudes == 0:
            return 0

        return dot_prod / producto_magnitudes


# Ejemplos de uso
def demo_operaciones_vectoriales():
    """
    Prueba las operaciones vectoriales con ejemplos de Machine Learning.
    """
    mensaje = "Ejemplos de Operaciones Vectoriales"
    print("#" * len(mensaje))
    print(mensaje)
    print("#" * len(mensaje))
    print("\n")

    # Ejemplo 1: Preferencias de usuarios
    print("=== Ejemplo 1: Preferencias de usuarios ===")
    print("   Cada usuario se corresponde con un vector que mapea sus preferencias en películas")
    print("   Vector([acción, comedia, drama])")
    print("\n")
    usuarios = [
        Vector([4, 2, 5]),
        Vector([3, 4, 2]),
        Vector([9, 1, 2]),
        Vector([3, 8, 1]),
        Vector([1, 2, 9])
    ]
    for index_i, usuario_i in enumerate(usuarios):
        print(f"   Usuario {index_i}: {usuario_i}")
        for index_j in range(index_i + 1, len(usuarios)):
            usuario_j = usuarios[index_j]
            print(f"      Cálculos de similitud con el usuario {index_j}")
            combinadas = usuario_i + usuario_j
            print(f"         Suma: preferencias combinadas: {combinadas}")
            similitud_producto_punto = usuario_i.producto_punto(usuario_j)
            print(f"         Similitud (producto punto): {similitud_producto_punto}")
            similitud_coseno = usuario_i.similitud_coseno(usuario_j)
            print(f"         Similitud coseno: {similitud_coseno:.3f}")
    print("\n")

    # Ejemplo 2: Vectores de características
    print("=== Ejemplo 2: Análisis de Documentos ===")
    print("   Cada documento se corresponde con un vector que mapea las frecuencias de las palabras que contiene")
    print("   Vector([frecuencia_palabra_1, frecuencia_palabra_2, frecuencia_palabra_3, frecuencia_palabra_4])")
    documento_1 = Vector([2, 1, 0, 3])  # Frecuencias de palabras
    documento_2 = Vector([1, 2, 1, 2])  # Frecuencias de palabras
    print(f"   Documento 1: {documento_1}")
    print(f"   Documento 2: {documento_2}")
    similitud_documentos_producto_punto = documento_1.producto_punto(documento_2)
    print(f"      Similitud (producto punto): {similitud_documentos_producto_punto}")
    similitud_documentos_coseno = documento_1.similitud_coseno(documento_2)
    print(f"      Similitud entre documentos (coseno): {similitud_documentos_coseno:.3f}")


if __name__ == "__main__":
    demo_operaciones_vectoriales()
