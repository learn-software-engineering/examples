"""
Curso:    Inteligencia Artificial
Módulo:   Algebra Lineal
Artículo: Vectores, Escalares y Espacios Vectoriales

Implementación en Python puro
Python 3.10+
"""
import numpy


###################################
# Operaciones vectoriales con Numpy
###################################

def suma_vectores(u: numpy.ndarray, v: numpy.ndarray) -> numpy.ndarray:
    return u + v


def multiplicacion_escalar(alpha: float, v: numpy.ndarray) -> numpy.ndarray:
    return alpha * v


def norma_l2(v: numpy.ndarray) -> float:
    """
    Norma euclidiana (L2): la longitud geométrica del vector v.
    Es el teorema de Pitágoras generalizado a n dimensiones.
    """
    return numpy.linalg.norm(v)


def norma_l1(v: numpy.ndarray) -> float:
    """
    Norma Manhattan (L1): suma de valores absolutos.
    Induce dispersión (sparsity), usada en regularización LASSO.
    """
    return numpy.linalg.norm(v, 1)


def producto_punto(u: numpy.ndarray, v: numpy.ndarray) -> float:
    return numpy.dot(u, v)


def similitud_coseno(u: numpy.ndarray, v: numpy.ndarray) -> float:
    norma_u = norma_l2(u)
    norma_v = norma_l2(v)
    # Protección contra división por cero (el vector cero no tiene dirección)
    if norma_u == 0 or norma_v == 0:
        raise ValueError("La similitud coseno no está definida para el vector cero.")
    return producto_punto(u, v) / (norma_u * norma_v)


def angulo_entre(u: numpy.ndarray, v: numpy.ndarray, grados: bool = True) -> float:
    """
    Ángulo entre dos vectores en radianes o grados.
    Usa: theta = arccos(similitud_coseno(u, v))
    """
    cos_theta = similitud_coseno(u, v)
    theta_rad = numpy.arccos(cos_theta)
    return numpy.degrees(theta_rad) if grados else theta_rad


def normalizar(v: numpy.ndarray) -> numpy.ndarray:
    magnitud = norma_l2(v)
    return v / magnitud

#########
# Ejemplo
#########

if __name__ == "__main__":
    # Dos vectores en 3 dimensiones
    # Imagínalos como embeddings de dos documentos
    u = numpy.array([1.0, 2.0, 3.0])
    v = numpy.array([4.0, 0.0, -1.0])

    print("=================================")
    print("Operaciones vectoriales con Numpy")
    print("=================================")
    print(f"u = {u}")
    print(f"v = {v}")
    print(f"Suma (u + v)                   -> {suma_vectores(u, v)}")
    print(f"Multiplicación escalar (2 * u) -> {multiplicacion_escalar(2.0, u)}")
    print(f"Norma L2 de u (||u||₂)         -> {norma_l2(u):.4f}")
    print(f"Norma L1 de u (||u||₁)         -> {norma_l1(u):.4f}")
    print(f"Producto punto (u · v)         -> {producto_punto(u, v):.4f}")
    print(f"Similitud coseno               -> {similitud_coseno(u, v):.4f}")
    print(f"Ángulo entre u y v             -> {angulo_entre(u, v):.2f}°")
    print(f"Vector unitario de u (û)       -> {[round(x, 4) for x in normalizar(u)]}")
    u_hat = normalizar(u)
    print(f"Verificar `||û||₂ = 1`         -> {norma_l2(u_hat):.6f}")

    print("==========================")
    print("Demo de analogía semántica")
    print("==========================")
    print("En NLP real, estos serían embeddings aprendidos por un modelo.")
    print("Aquí ilustramos el principio con vectores de características")
    print("creados manualmente.")
    print("Características: [realeza, masculinidad, edad_relativa, poder]")
    rey = numpy.array([0.9, 0.9, 0.8, 0.9])
    reina = numpy.array([0.9, 0.1, 0.8, 0.9])
    hombre = numpy.array([0.0, 0.9, 0.5, 0.4])
    mujer = numpy.array([0.0, 0.1, 0.5, 0.4])
    print(f"rey    = {rey}")
    print(f"reina  = {reina}")
    print(f"hombre = {hombre}")
    print(f"mujer  = {mujer}")

    print("La famosa analogía: rey - hombre + mujer ≈ reina")
    vector_analogia = suma_vectores(
        suma_vectores(rey, multiplicacion_escalar(-1.0, hombre)),
        mujer
    )
    sim_reina = similitud_coseno(vector_analogia, reina)
    sim_rey = similitud_coseno(vector_analogia, rey)

    print(f"rey - hombre + mujer -> {[round(x, 2) for x in vector_analogia]}")
    print(f"Similitud coseno con 'reina': {sim_reina:.4f}")
    print(f"Similitud coseno con 'rey':   {sim_rey:.4f}")
    print("==> El vector de analogía está más cerca de 'reina' que de 'rey'.")
