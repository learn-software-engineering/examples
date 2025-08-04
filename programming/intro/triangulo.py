# Entrada del usuario
lado1 = float(input("Introduce la longitud del primer lado: "))
lado2 = float(input("Introduce la longitud del segundo lado: "))
lado3 = float(input("Introduce la longitud del tercer lado: "))

# Cálculo del perímetro
perimetro = lado1 + lado2 + lado3

# Cálculo del área usando la fórmula de Herón
s = perimetro / 2
area = (s*(s-lado1)*(s-lado2)*(s-lado3)) ** 0.5

print(f"El perímetro del triángulo es: {perimetro}")
print(f"El área del triángulo es: {area:.2f}")
