import matplotlib.pyplot as plt


from sistema_recomendaciones import SistemaDeRecomendaciones


# Crear y probar el sistema de recomendación
def demostracion_del_sistema():
    """
    Prueba completa del sistema de recomendación.

    Este proyecto demuestra cómo el álgebra lineal es fundamental en:
    1. Representación de datos (vectores de usuarios/items)
    2. Cálculo de similitudes (producto punto, normas)
    3. Reducción de dimensionalidad (PCA, descomposición en autovalores)
    4. Predicción y recomendación (filtrado colaborativo)
    """
    mensaje = "=== Prueba del Sistema de Recomendación ==="
    print("=" * len(mensaje))
    print(mensaje)
    print("=" * len(mensaje))

    # Crear el sistema
    sistema_de_recomendaciones = SistemaDeRecomendaciones()

    # Generar reporte
    sistema_de_recomendaciones.imprimir_reporte_completo()

    # Hacer recomendaciones para cada usuario
    print()
    mensaje = "Hacer recomendaciones para los usuarios"
    print("*"*len(mensaje))
    print(mensaje)
    print("*"*len(mensaje))


# Punto de entrada principal
if __name__ == "__main__":
    demostracion_del_sistema()
