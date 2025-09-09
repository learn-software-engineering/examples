from sistema_recomendaciones import SistemaRecomendaciones


def ejecutar_demostracion_completa():
    """
    DEMOSTRACIÓN COMPLETA DEL SISTEMA
    Esta función muestra todas las capacidades del sistema de recomendaciones.
    Es perfecta para entender cómo funciona cada componente.
    """
    message = "Sistema de Recomendaciones - Demostración Completa"
    print(message)
    print("=" * len(message))

    try:
        # Inicializar sistema
        sistema = SistemaRecomendaciones(
            archivo_config="config.yaml", ruta_datos="datos/")

        # Análisis general del sistema
        message = "Estadísticas del Sistema"
        print("\n")
        print("=" * len(message))
        print(message)
        print("=" * len(message))
        estadisticas = sistema.analizar_sistema()

        print("\n")
        print(f"Usuarios: {estadisticas['usuarios']['total']}")
        print(f"   * Por género: {dict(estadisticas['usuarios']['por_genero'])}")
        print(f"   * Por ubicación: {dict(estadisticas['usuarios']['por_ubicacion'])}")
        print(f"   * Por nivel de gasto: {dict(estadisticas['usuarios']['por_nivel_gasto'])}")
        print(f"   * Edad promedio: {estadisticas['usuarios']['edad_promedio']:.1f} años")

        print(f"Productos: {estadisticas['productos']['total']}")
        print(f"   * Por categoría: {dict(estadisticas['productos']['por_categoria'])}")
        print(f"   * Precio promedio: ${estadisticas['productos']['precio_promedio']:,.0f}")
        print(f"   * Calificación promedio: {estadisticas['productos']['valoracion_promedio']:.2f}/5")

        print(f"Interacciones: {estadisticas['interacciones']['total']}")
        print(f"   * Por tipo: {dict(estadisticas['interacciones']['por_tipo'])}")
        print(f"   * Por usuario: {dict(estadisticas['interacciones']['por_usuario'])}")
        print(f"   * Usuarios activos: {estadisticas['interacciones']['usuarios_activos']}")

        if 'similitudes' in estadisticas:
            print("Similitudes:")
            print(f"   * Promedio: {estadisticas['similitudes']['promedio']:.3f}")
            print(f"   * Máxima: {estadisticas['similitudes']['maxima']:.3f}")
            print(f"   * Mínima: {estadisticas['similitudes']['minima']:.3f}")

        # Generar recomendaciones para cada usuario
        print("\n")
        for id_usuario in sistema.usuarios.keys():
            sistema.imprimir_reporte_detallado(id_usuario)
            print("\n")

        print("\n")
        message = "Demostración Completada Exitosamente!"
        print("=" * len(message))
        print(message)
        print("Revisa los reportes anteriores para entender cómo funciona cada componente")
        print("=" * len(message))

    except Exception as e:
        print(f"Error durante la demostración: {str(e)}")


def ejecutar_comparacion_algoritmos():
    """
    COMPARACIÓN ENTRE ALGORITMOS
    Muestra las diferencias entre filtrado colaborativo y por contenido
    para ayudar a entender cuándo usar cada uno.
    """
    message = "Comparación de Algoritmos"
    print("=" * len(message))
    print(message)
    print("=" * len(message))

    sistema = SistemaRecomendaciones(
        archivo_config="config.yaml", ruta_datos="datos/")
    usuario_test = "user_001"

    print(f"Usuario de prueba: {sistema.usuarios[usuario_test]['nombre']}")

    # Recomendaciones colaborativas
    print("Recomendaciones por filtrado colaborativo:")
    rec_colab = sistema.recomendar_por_filtrado_colaborativo(usuario_test, 5)
    for i, (prod_id, puntuacion) in enumerate(rec_colab, 1):
        producto = sistema.productos[prod_id]
        print(f"   {i}. {producto['nombre']} (Puntuación: {puntuacion:.3f})")

    # Recomendaciones por contenido
    print("Recomendaciones por filtrado por contenido:")
    rec_contenido = sistema.recomendar_por_contenido(usuario_test, 5)
    for i, (prod_id, puntuacion) in enumerate(rec_contenido, 1):
        producto = sistema.productos[prod_id]
        print(f"   {i}. {producto['nombre']} (Puntuación: {puntuacion:.3f})")

    # Sistema híbrido
    print("Sistema híbrido")
    rec_hibrido = sistema.generar_recomendaciones(usuario_test, 5, incluir_explicacion=False)
    for producto in rec_hibrido['productos']:
        print(f"   {producto['ranking']}. {producto['nombre']} (Puntuación: {producto['puntuacion']})")

    print("Observaciones")
    print("   * Colaborativo: Basado en usuarios similares")
    print("   * Contenido: Basado en perfil del usuario")
    print("   * Híbrido: Combina ambos enfoques")


if __name__ == "__main__":
    """
    Esta es la funcion es la encargada de iniciar el sistema
    y mostrar su ejecución.
    """
    print("Selecciona el tipo de demostración:")
    print("   1- Demostración completa")
    print("   2- Comparación de algoritmos")
    print("   3- Usuario específico")

    try:
        opcion = input("\nOpción (1-3): ").strip()

        if opcion == "1":
            ejecutar_demostracion_completa()
        elif opcion == "2":
            ejecutar_comparacion_algoritmos()
        elif opcion == "3":
            sistema = SistemaRecomendaciones(
                archivo_config="config.yaml", ruta_datos="datos/")
            print("\nUsuarios disponibles:")
            for uid, user in sistema.usuarios.items():
                print(f"   {uid}: {user['nombre']}")

            usuario_id = input("\nIngresa ID de usuario: ").strip()
            sistema.imprimir_reporte_detallado(usuario_id)
        else:
            print("Opción inválida")

    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("   Asegúrate de tener los archivos de datos correctos")
