"""
Course:  Artificial Intelligence
Módulo:  Linear Algebra
Article: Vectors, Scalars & Vector Spaces

NumPy implementation
Python 3.10+
"""
import numpy


##############################
# Vector operations with Numpy
##############################

def vector_add(u: numpy.ndarray, v: numpy.ndarray) -> numpy.ndarray:
    return u + v


def scalar_multiply(alpha: float, v: numpy.ndarray) -> numpy.ndarray:
    return alpha * v


def l2_norm(v: numpy.ndarray) -> float:
    """
    Euclidean (L2) norm: the geometric length of vector v.
    """
    return numpy.linalg.norm(v)


def l1_norm(v: numpy.ndarray) -> float:
    """
    Manhattan (L1) norm: sum of absolute values.
    Sparsity-inducing, used in LASSO regularization.
    """
    return numpy.linalg.norm(v, 1)


def dot_product(u: numpy.ndarray, v: numpy.ndarray) -> float:
    return numpy.dot(u, v)


def cosine_similarity(u: numpy.ndarray, v: numpy.ndarray) -> float:
    norm_u = l2_norm(u)
    norm_v = l2_norm(v)
    # Guard against division by zero (zero vector has no direction)
    if norm_u == 0 or norm_v == 0:
        raise ValueError("Cosine similarity undefined for zero vectors.")
    return dot_product(u, v) / (norm_u * norm_v)


def angle_between(u: numpy.ndarray, v: numpy.ndarray, degrees: bool = True) -> float:
    """
    Angle between two vectors in radians or degrees.
    Uses: theta = arccos(cosine_similarity(u, v))
    """
    cos_theta = cosine_similarity(u, v)
    theta_rad = numpy.arccos(cos_theta)
    return numpy.degrees(theta_rad) if degrees else theta_rad


def normalize(v: numpy.ndarray) -> numpy.ndarray:
    magnitude = l2_norm(v)
    return v / magnitude


#########
# Example
#########

if __name__ == "__main__":
    # Two 3-dimensional vectors — imagine these as two user embeddings
    u = numpy.array([1.0, 2.0, 3.0])
    v = numpy.array([4.0, 0.0, -1.0])

    print("============================")
    print("Vector Operations with Numpy")
    print("============================")
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

    king = numpy.array([0.9, 0.9, 0.8, 0.9])
    queen = numpy.array([0.9, 0.1, 0.8, 0.9])
    man = numpy.array([0.0, 0.9, 0.5, 0.4])
    woman = numpy.array([0.0, 0.1, 0.5, 0.4])
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
