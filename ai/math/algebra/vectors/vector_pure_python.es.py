"""
Curso:    Inteligencia Artificial
Módulo:   Algebra Lineal
Artículo: Vectores, Escalares y Espacios Vectoriales

Implementación en NumPy
Python 3.10+
"""
import math
from typing import List


#########################
# Operaciones vectoriales
#########################

def suma_vectores(u: List[float], v: List[float]) -> List[float]:
    """
    Suma dos vectores componente a componente.
    Requiere: u y v tienen la misma dimensión.
    """
    assert len(u) == len(v), f"Error de dimensión: {len(u)} vs {len(v)}"
    return [u_i + v_i for u_i, v_i in zip(u, v)]


def multiplicacion_escalar(alpha: float, v: List[float]) -> List[float]:
    """
    Multiplica un vector por un escalar.
    Estira/encoge la flecha; un alpha negativo la invierte 180°.
    """
    return [alpha * v_i for v_i in v]


def norma_l2(v: List[float]) -> float:
    """
    Norma euclidiana (L2): la longitud geométrica del vector v.
    Es el teorema de Pitágoras generalizado a n dimensiones.
    """
    return math.sqrt(sum(v_i ** 2 for v_i in v))


def norma_l1(v: List[float]) -> float:
    """
    Norma Manhattan (L1): suma de valores absolutos.
    Induce dispersión (sparsity), usada en regularización LASSO.
    """
    return sum(abs(v_i) for v_i in v)


def producto_punto(u: List[float], v: List[float]) -> float:
    """
    Producto punto: suma de productos componente a componente.
    Devuelve un escalar que mide cuánto se 'alinean' u y v.
    Requiere: u y v tienen la misma dimensión.
    """
    assert len(u) == len(v), f"Error de dimensión: {len(u)} vs {len(v)}"
    return sum(u_i * v_i for u_i, v_i in zip(u, v))


def similitud_coseno(u: List[float], v: List[float]) -> float:
    """
    Similitud coseno: producto_punto(u,v) / (||u|| * ||v||).
    Devuelve un valor en [-1, 1].
      1.0  -> misma dirección (similitud máxima)
      0.0  -> ortogonales (sin relación)
     -1.0  -> direcciones opuestas (totalmente disímiles)
    """
    norma_u = norma_l2(u)
    norma_v = norma_l2(v)
    # Protección contra división por cero (el vector cero no tiene dirección)
    if norma_u == 0 or norma_v == 0:
        raise ValueError("La similitud coseno no está definida para el vector cero.")
    return producto_punto(u, v) / (norma_u * norma_v)


def angulo_entre(u: List[float], v: List[float], grados: bool = True) -> float:
    """
    Ángulo entre dos vectores en radianes o grados.
    Usa: theta = arccos(similitud_coseno(u, v))

    IMPORTANTE: aplicamos 'clamp' antes de arccos para evitar errores
    de punto flotante que empujan cos ligeramente fuera de [-1, 1].
    """
    cos_theta = similitud_coseno(u, v)
    cos_theta = max(-1.0, min(1.0, cos_theta))  # clamp numérico
    theta_rad = math.acos(cos_theta)
    return math.degrees(theta_rad) if grados else theta_rad


def normalizar(v: List[float]) -> List[float]:
    """
    Devuelve el vector unitario (longitud 1) que apunta en la
    misma dirección que v.
    Fórmula: v_hat = v / ||v||

    Los vectores unitarios son útiles cuando importa la DIRECCIÓN,
    no la magnitud. En similitud coseno solo importa la dirección,
    así que trabajar con vectores normalizados es equivalente
    y computacionalmente más eficiente.
    """
    norma = norma_l2(v)
    if norma == 0:
        raise ValueError("No se puede normalizar el vector cero.")
    return [v_i / norma for v_i in v]


#########
# Ejemplo
#########

if __name__ == "__main__":
    # Dos vectores en 3 dimensiones
    # Imagínalos como embeddings de dos documentos
    u = [1.0, 2.0, 3.0]
    v = [4.0, 0.0, -1.0]

    print("=======================================")
    print("Operaciones vectoriales con Python puro")
    print("=======================================")
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
    rey = [0.9, 0.9, 0.8, 0.9]
    reina = [0.9, 0.1, 0.8, 0.9]
    hombre = [0.0, 0.9, 0.5, 0.4]
    mujer = [0.0, 0.1, 0.5, 0.4]
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
