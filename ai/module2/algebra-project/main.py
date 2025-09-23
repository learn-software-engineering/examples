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


    for id_usuario in list(sistema_de_recomendaciones.ids_usuarios):
        usuario = sistema_de_recomendaciones.usuarios[id_usuario]
        print(f"   Recomendaciones para {usuario.obtener_nombre()}:")
        try:
            recomendaciones = sistema_de_recomendaciones.generar_recomendaciones(id_usuario, 3)
            if recomendaciones:
                for j, (id_pelicula, prediccion) in enumerate(recomendaciones, 1):
                    nombre_pelicula = sistema_de_recomendaciones.peliculas[id_pelicula]["nombre"]
                    print(f"      {j}- {nombre_pelicula} - Predicción de puntuación {prediccion:.2f}")
            else:
                print("      - No hay recomendaciones disponibles")
        except Exception as e:
            print(f"      - Error: {e}")


# Punto de entrada principal
if __name__ == "__main__":
    demostracion_del_sistema()
