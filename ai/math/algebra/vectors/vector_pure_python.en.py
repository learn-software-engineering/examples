"""
Course:  Artificial Intelligence
Módulo:  Linear Algebra
Article: Vectors, Scalars & Vector Spaces

Pure Python implementation
Python 3.10+
"""
import math
from typing import List


###################
# Vector operations
###################

def vector_add(u: List[float], v: List[float]) -> List[float]:
    """
    Add two vectors element-wise.
    Requires: u and v have the same dimension.
    """
    assert len(u) == len(v), f"Dimension mismatch: {len(u)} vs {len(v)}"
    return [u_i + v_i for u_i, v_i in zip(u, v)]


def scalar_multiply(alpha: float, v: List[float]) -> List[float]:
    """
    Multiply a vector by a scalar.
    Stretches/shrinks the arrow; negative alpha flips its direction.
    """
    return [alpha * v_i for v_i in v]


def l2_norm(v: List[float]) -> float:
    """
    Euclidean (L2) norm: the geometric length of vector v.
    """
    return math.sqrt(sum(v_i ** 2 for v_i in v))


def l1_norm(v: List[float]) -> float:
    """
    Manhattan (L1) norm: sum of absolute values.
    Sparsity-inducing, used in LASSO regularization.
    """
    return sum(abs(v_i) for v_i in v)


def dot_product(u: List[float], v: List[float]) -> float:
    """
    Dot product: sum of element-wise products.
    Returns a scalar measuring how much u and v 'align'.
    Requires: u and v have the same dimension.
    """
    assert len(u) == len(v), f"Dimension mismatch: {len(u)} vs {len(v)}"
    return sum(u_i * v_i for u_i, v_i in zip(u, v))


def cosine_similarity(u: List[float], v: List[float]) -> float:
    """
    Cosine similarity: dot(u,v) / (||u|| * ||v||).
    Returns a value in [-1, 1].
      1.0  -> identical direction (maximally similar)
      0.0  -> orthogonal (unrelated)
     -1.0  -> opposite direction (maximally dissimilar)
    """
    norm_u = l2_norm(u)
    norm_v = l2_norm(v)
    # Guard against division by zero (zero vector has no direction)
    if norm_u == 0 or norm_v == 0:
        raise ValueError("Cosine similarity undefined for zero vectors.")
    return dot_product(u, v) / (norm_u * norm_v)


def angle_between(u: List[float], v: List[float], degrees: bool = True) -> float:
    """
    Angle between two vectors in radians or degrees.
    Uses: theta = arccos(cosine_similarity(u, v))
    Clamp to [-1, 1] first to guard against floating-point errors
    that push cos slightly outside the valid domain of arccos.
    """
    cos_theta = cosine_similarity(u, v)
    cos_theta = max(-1.0, min(1.0, cos_theta))  # numerical clamp
    theta_rad = math.acos(cos_theta)
    return math.degrees(theta_rad) if degrees else theta_rad


def normalize(v: List[float]) -> List[float]:
    """
    Return the unit vector (length 1) pointing in the same direction as v.
    Formula: v_hat = v / ||v||
    Unit vectors are useful when you care about DIRECTION, not magnitude.
    """
    norm = l2_norm(v)
    if norm == 0:
        raise ValueError("Cannot normalize the zero vector.")
    return [v_i / norm for v_i in v]


#########
# Example
#########

if __name__ == "__main__":
    # Two 3-dimensional vectors, imagine these as two user embeddings
    u = [1.0, 2.0, 3.0]
    v = [4.0, 0.0, -1.0]

    print("==================================")
    print("Vector Operations with pure Python")
    print("==================================")
    print(f"u = {u}")
    print(f"v = {v}")

    print(f"Addition (u + v)        -> {vector_add(u, v)}")
    print(f"Scalar multiply (2 * u) -> {scalar_multiply(2.0, u)}")
    print(f"L2 norm of u (||u||₂)   -> {l2_norm(u):.4f}")
    print(f"L1 norm of u (||u||₁)   -> {l1_norm(u):.4f}")
    print(f"Dot product (u · v)     -> {dot_product(u, v):.4f}")
    print(f"Cosine similarity       -> {cosine_similarity(u, v):.4f}")
    print(f"Angle between u, v.     -> {angle_between(u, v):.2f}°")
    print(f"Unit vector of u (û)    -> {[round(x, 4) for x in normalize(u)]}")
    u_hat = normalize(u)
    print(f"Verify `||û||₂ = 1`     -> {l2_norm(u_hat):.6f}")

    print("=============================")
    print("Semantic similarity mini-demo")
    print("=============================")
    print("In real NLP, these would be word embeddings. Here we illustrate")
    print("the principle with handcrafted feature vectors.")
    print("Features: [royalty_score, masculinity, age, power]")

    king = [0.9, 0.9, 0.8, 0.9]
    queen = [0.9, 0.1, 0.8, 0.9]
    man = [0.0, 0.9, 0.5, 0.4]
    woman = [0.0, 0.1, 0.5, 0.4]
    print(f"king  = {king}")
    print(f"queen = {queen}")
    print(f"man   = {man}")
    print(f"woman = {woman}")

    print("The famous analogy: king - man + woman ≈ queen")
    analogy_vec = vector_add(
        vector_add(king, scalar_multiply(-1.0, man)),
        woman
    )
    sim_to_queen = cosine_similarity(analogy_vec, queen)
    sim_to_king = cosine_similarity(analogy_vec, king)

    print(f"king − man + woman -> {[round(x,2) for x in analogy_vec]}")
    print(f"Cosine similarity to 'queen': {sim_to_queen:.4f}")
    print(f"Cosine similarity to 'king':  {sim_to_king:.4f}")
    print("==> The analogy vector is closer to 'queen' than 'king'.")
