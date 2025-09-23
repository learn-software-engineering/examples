import os
import json
from typing import Dict, List, Optional, Tuple

import numpy as np
from prettytable import PrettyTable

from usuario import Usuario


class SistemaDeRecomendaciones:
    """
    Sistema de recomendaciones basado en álgebra lineal.

    Este proyecto demuestra cómo el álgebra lineal es fundamental
    en sistemas de machine learning reales.

    Fundamentos teóricos:
    =====================

    1. Espacios vectoriales:
       - Cada usuario es un vector en R^n (donde n = número de películas)
       - Las puntuaciones son las coordenadas del vector
       - El espacio completo contiene todos los usuarios posibles

    2. Similitud entre vectores:
       - Similitud coseno: cos(θ) = (u·v) / (||u|| ||v||)
       - Producto punto: u·v = Σ(ui * vi)
       - Distancia euclidiana: ||u-v|| = √(Σ(ui-vi)²)

    3. Filtrado colaborativo:
       - Usuarios similares tienen gustos similares
       - Si A y B son similares, y A le gusta X, entonces B probablemente le guste X
       - Matemáticamente: predicción = Σ(similitud * puntuación) / Σ(similitud)

    4. Reducción de dimensionalidad (PCA):
       - Los gustos de usuarios se pueden representar en menos dimensiones
       - Ejemplo: dimensiones latentes como "acción vs drama" o "mainstream vs indie"
       - Descomposición en valores propios de la matriz de covarianza encuentra estas dimensiones
    """

    def __init__(self, ruta_datos: str = "datos/"):
        """
        Inicialización del sistema
        Args:
            ruta_datos: Carpeta donde están los archivos JSON con los datos

        ¿Por qué separamos los datos del código?
        - Facilita testing con diferentes datasets
        - Permite actualizar datos sin tocar la lógica
        - Hace el código más mantenible y escalable
        """
        print("Inicializando el sistema")

        # Estructuras de datos principales
        self.usuarios: List[str, Usuario] = {}
        self.peliculas: Dict[str, Dict] = {}
        self.interacciones: List[Dict] = []

        # Estructuras matriciales para álgebra lineal
        self.ids_usuarios: List[str] = []
        self.ids_peliculas: List[str] = []
        self.matriz_puntuaciones: Optional[np.ndarray] = None
        self.matriz_similitud_usuarios: Optional[np.ndarray] = None

        # Cargar datos
        self._cargar_datos(ruta_datos)
        # Crear la matriz de recomendaciones
        self._construir_matriz_puntuaciones()
        # Crear la matriz de similitud entre usuarios
        self._construir_matriz_similitud()

        print("Sistema de recomendaciones inicializado correctamente")
        print("")

    def _cargar_datos(self, ruta_datos: str = "datos/"):
        """
        Carga de datos desde archivos externos.

        Patrón de diseño: Separación de Responsabilidades
        Los datos están separados de la lógica, facilitando mantenimiento

        ¿Por qué usamos archivos JSON?
        - Formato estándar para intercambio de datos
        - Fácil de leer y modificar manualmente
        - Compatible con APIs REST
        - Permite versionado de datos
        """
        try:
            # Cargar peliculas
            with open(os.path.join(ruta_datos, "peliculas.json"), "r", encoding="utf-8") as f:
                datos_peliculas_json = json.load(f)
                self.peliculas = datos_peliculas_json["peliculas"]
                self.ids_peliculas = list(self.peliculas.keys())
                print(f"   * {len(self.peliculas)} peliculas cargadas")

            # Cargar usuarios
            # Creo un objecto del tipo usuario por cada uno cargado
            with open(os.path.join(ruta_datos, "usuarios.json"), "r", encoding="utf-8") as f:
                datos_usuarios_json = json.load(f)
                datos_usuarios = datos_usuarios_json["usuarios"]
                for id_usuario, datos_usuario in datos_usuarios.items():
                    self.usuarios[id_usuario] = Usuario(id_usuario, datos_usuario["nombre"], len(self.peliculas))
                    self.ids_usuarios.append(id_usuario)
                print(f"   * {len(self.usuarios)} usuarios cargados")

            # Cargar interacciones
            with open(os.path.join(ruta_datos, "interacciones.json"), "r", encoding="utf-8") as f:
                datos_interacciones_json = json.load(f)
                self.interacciones = datos_interacciones_json["interacciones"]
                print(f"   * {len(self.interacciones)} interacciones cargadas")

            # Procesar interacciones para llenar vectores de puntuaciones
            self._procesar_interacciones()

        except FileNotFoundError as e:
            print(f"Error: No se encontró el archivo {e.filename}")
            print("Asegúrate de tener los archivos usuarios.json, peliculas.json e interacciones.json")
            raise
        except json.JSONDecodeError as e:
            print(f"Error al leer JSON: {e}")
            raise

    def _procesar_interacciones(self):
        """
        Procesa las interacciones para llenar los vectores de puntuaciones.

        Concepto: Construcción del espacio vectorial de usuarios
        - Cada interacción actualiza una componente del vector usuario
        - El resultado es una representación vectorial completa de preferencias
        """
        print("   Procesando interacciones...")
        for interaccion in self.interacciones:
            id_usuario = interaccion["usuario"]
            nombre_pelicula = interaccion["pelicula"]
            puntuacion = interaccion["puntuacion"]

            # Encontrar el índice de la película en nuestro vector
            if nombre_pelicula in self.ids_peliculas:
                indice_pelicula = self.ids_peliculas.index(nombre_pelicula)
                # Actualizar el vector del usuario
                self.usuarios[id_usuario].actualizar_puntuacion_de_pelicula(indice_pelicula, puntuacion)

        print("   Vectores de usuarios actualizados")

    def _construir_matriz_puntuaciones(self) -> np.ndarray:
        """
        Construye la matriz de puntuaciones usuarios x películas.

        Concepto: Matriz de puntuaciones R
        ===============================================

        R es una matriz m x n donde:
        - m = número de usuarios
        - n = número de películas
        - R[i,j] = puntuación del usuario i para la película j
        - R[i,j] = 0 si el usuario i no ha visto la película j

        Esta matriz es la representación completa de nuestro sistema:

        Películas:  A    B    C    D
        Usuario 1: [4.5, 0.0, 3.0, 5.0]
        Usuario 2: [2.0, 4.0, 0.0, 3.5]
        Usuario 3: [5.0, 1.0, 4.0, 0.0]

        Propiedades matemáticas importantes:
        - Usualmente es una matriz dispersa (muchos ceros)
        - Cada fila es el vector de un usuario
        - Cada columna representa las puntuaciones de una película
        """
        # Inicializar con ceros la matriz de puntuaciones
        self.matriz_puntuaciones = np.zeros((len(self.ids_usuarios), len(self.ids_peliculas)))

        # Llenar la matriz con las puntuaciones de cada usuario
        for index, id_usuario in enumerate(self.ids_usuarios):
            usuario = self.usuarios[id_usuario]
            self.matriz_puntuaciones[index] = usuario.obtener_vector_puntuaciones()

        print(f"   Matriz de puntuaciones construida: {self.matriz_puntuaciones.shape}")
        return self.matriz_puntuaciones

    def _calcular_similitud_coseno(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        Calcula la similitud coseno entre dos vectores.

        Fórmula: cos(θ) = (A·B) / (||A|| ||B||)

        Interpretación geométrica:
        - cos(0°) = 1.0    -> vectores idénticos (gustos idénticos)
        - cos(90°) = 0.0   -> vectores ortogonales (gustos no relacionados)
        - cos(180°) = -1.0 -> vectores opuestos (gustos opuestos)

        Args:
            vector1, vector2: Vectores de puntuaciones a comparar

        Returns:
            float: Similitud coseno entre -1 y 1
        """
        # Calcular normas (magnitudes) de los vectores
        norma1 = np.linalg.norm(vector1)
        norma2 = np.linalg.norm(vector2)

        # Evitar división por cero
        if norma1 == 0 or norma2 == 0:
            return 0.0

        # Calcular producto punto y normalizar
        producto_punto = np.dot(vector1, vector2)
        similitud = producto_punto / (norma1 * norma2)

        return similitud

    def _construir_matriz_similitud(self) -> np.ndarray:
        """
        Construye la matriz de similitud (coseno) entre todos los usuarios.

        Concepto: Matriz de Similitud S
        ===============================

        S es una matriz simétrica m x m donde:
        - S[i,j] = similitud entre usuario i y usuario j
        - S[i,i] = 1.0 (un usuario es idéntico a sí mismo)
        - S[i,j] = S[j,i] (la similitud es simétrica)

        Esta matriz captura las relaciones entre usuarios:

                Usuario1  Usuario2  Usuario3
        Usuario1   1.000     0.650     0.230
        Usuario2   0.650     1.000     0.180
        Usuario3   0.230     0.180     1.000

        Returns:
            np.ndarray: Matriz de similitud m x m
        """
        if self.matriz_puntuaciones is None:
            self._construir_matriz_puntuaciones()

        numero_de_usuarios = len(self.usuarios)
        self.matriz_similitud_usuarios = np.zeros((numero_de_usuarios, numero_de_usuarios))

        print(f"   Calculando similitudes entre {numero_de_usuarios} usuarios")

        for i in range(numero_de_usuarios):
            for j in range(i, numero_de_usuarios):  # Solo calculamos triángulo superior (matriz simétrica)
                if i == j:  # Un usuario es idéntico a sí mismo
                    similitud = 1.0
                else:
                    vector_i = self.matriz_puntuaciones[i]
                    vector_j = self.matriz_puntuaciones[j]
                    similitud = self._calcular_similitud_coseno(vector_i, vector_j)

                # Llenar matriz simétrica
                self.matriz_similitud_usuarios[i, j] = similitud
                self.matriz_similitud_usuarios[j, i] = similitud

        print(f"   Matriz de similitud entre usuarios construida: {self.matriz_similitud_usuarios.shape}")
        return self.matriz_similitud_usuarios

    def predecir_puntuacion(self, id_usuario: str, id_pelicula: str, k: int = 5) -> float:
        """
        Predice la puntuación que un usuario daría a una película.

        Algoritmo: Filtrado Colaborativo basado en usuarios
          1. Encontrar los k usuarios más similares al usuario objetivo
          2. De esos usuarios, considerar solo los que vieron la película
          3. Calcular predicción ponderada por similitud:
              predicción = Σ(similitud[i] x puntuación[i]) / Σ(similitud[i])

        Concepto: Si usuarios similares a ti puntuaron bien una película,
        probablemente tú también la puntuarías bien.

        Args:
            id_usuario: ID del usuario para quien predecir
            id_pelicula: Nombre de la película a predecir
            k: Número de usuarios similares a considerar

        Returns:
            float: Puntuación predicha (0.0 si no se puede predecir)
        """
        if id_usuario not in self.usuarios:
            raise ValueError(f"Usuario '{id_usuario}' no encontrado")

        if id_pelicula not in self.ids_peliculas:
            raise ValueError(f"Película con el ID '{id_pelicula}' no encontrada")

        if self.matriz_similitud_usuarios is None:
            self._construir_matriz_similitud()

        # Índices en las matrices
        indice_usuario = self.ids_usuarios.index(id_usuario)
        indice_pelicula = self.ids_peliculas.index(id_pelicula)
        pelicula = self.peliculas[id_pelicula]
        nombre_pelicula = pelicula["nombre"]

        # Verificar si el usuario ya vio la película
        puntuacion_almacenada = self.matriz_puntuaciones[indice_usuario, indice_pelicula]
        if puntuacion_almacenada > 0:
            print(f"   El usuario {id_usuario} ya calificó '{nombre_pelicula}' con {puntuacion_almacenada}")
            return puntuacion_almacenada

        # Obtener similitudes con todos los usuarios
        similitudes = self.matriz_similitud_usuarios[indice_usuario].copy()
        similitudes[indice_usuario] = 0  # Excluir al usuario

        # Encontrar usuarios que vieron la película
        usuarios_que_vieron = self.matriz_puntuaciones[:, indice_pelicula] > 0

        # Combinar: usuarios similares que vieron la película
        usuarios_relevantes = similitudes * usuarios_que_vieron

        # Seleccionar top-k usuarios más similares
        indices_topk = np.argsort(usuarios_relevantes)[-k:]
        indices_topk = indices_topk[usuarios_relevantes[indices_topk] > 0]  # Solo positivos

        if len(indices_topk) == 0:
            print(f"      No hay usuarios similares que hayan visto '{nombre_pelicula}'")
            return 0.0

        # Calcular predicción ponderada
        numerador = 0.0
        denominador = 0.0

        for i in indices_topk:
            similitud = similitudes[i]
            puntuacion = self.matriz_puntuaciones[i, indice_pelicula]
            numerador += similitud * puntuacion
            denominador += similitud

        if denominador == 0:
            return 0.0

        prediccion = numerador / denominador

        print(f"      Predicción para {id_usuario} - '{nombre_pelicula}': {prediccion:.2f} - Basada en {len(indices_topk)} usuarios similares")

        return prediccion

    def generar_recomendaciones(self, id_usuario: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Genera recomendaciones personalizadas para un usuario.

        Algoritmo:
          1. Identificar películas no vistas por el usuario
          2. Predecir calificaciones para esas películas
          3. Ordenar por calificación predicha descendente
          4. Retornar las top-N recomendaciones

        Args:
            id_usuario: Usuario para quien generar recomendaciones
            k: Número de recomendaciones a generar

        Returns:
            List[Tuple[str, float]]: Lista de (película, predicción) ordenadas
        """
        if id_usuario not in self.usuarios:
            raise ValueError(f"Usuario '{id_usuario}' no encontrado")

        usuario = self.usuarios[id_usuario]
        peliculas_vistas = usuario.obtener_peliculas_vistas()

        print(f"      Películas ya vistas: {len(peliculas_vistas)}/{len(self.ids_peliculas)}")

        # Películas no vistas
        ids_peliculas_no_vistas = []
        for i, pelicula in enumerate(self.peliculas):
            if i not in peliculas_vistas:
                ids_peliculas_no_vistas.append(pelicula)

        if not ids_peliculas_no_vistas:
            print("      El usuario ya vio todas las películas disponibles")
            return []

        # Predecir calificaciones para películas no vistas
        predicciones = []
        for id_pelicula in ids_peliculas_no_vistas:
            prediccion = self.predecir_puntuacion(id_usuario, id_pelicula)
            if prediccion > 0:  # Solo incluir predicciones válidas
                predicciones.append((id_pelicula, prediccion))

        # Ordenar por calificación predicha descendente
        predicciones.sort(key=lambda x: x[1], reverse=True)

        # Retornar top-N recomendaciones
        recomendaciones = predicciones[:k]

        print(f"      {len(recomendaciones)} recomendaciones generadas")

        return recomendaciones

    def imprimir_reporte_completo(self):
        """
        Genera un reporte completo del sistema de recomendaciones.
        """
        mensaje = "Reporte completo del sistema"
        print("*"*len(mensaje))
        print(mensaje)
        print("*"*len(mensaje))

        # Información básica
        print("Información del conjunto de datos:")
        print(f"   * Usuarios: {len(self.usuarios)}")
        print(f"   * Películas: {len(self.peliculas)}")
        print(f"   * Interacciones totales: {len(self.interacciones)}")

        if self.matriz_puntuaciones is not None:
            puntuaciones_dadas = np.count_nonzero(self.matriz_puntuaciones)
            puntuaciones_posibles = self.matriz_puntuaciones.size
            sparsity = 1 - (puntuaciones_dadas / puntuaciones_posibles)
            print(f"   * Calificaciones dadas: {puntuaciones_dadas:,} de {puntuaciones_posibles:,}")
            print(f"   * Sparsity (densidad): {sparsity:.1%}")

        # Usuarios
        print("")
        print("Análisis de los usuario")
        for id_usuario in self.ids_usuarios:
            usuario = self.usuarios[id_usuario]
            peliculas_vistas = usuario.obtener_peliculas_vistas()
            vector_de_puntuaciones = usuario.obtener_vector_puntuaciones()
            puntuacion_promedio = np.mean(vector_de_puntuaciones[vector_de_puntuaciones > 0])

            print(f"   * {usuario._nombre} (ID: {id_usuario}):")
            print(f"      - Películas vistas: {len(peliculas_vistas)}")
            print(f"      - Puntuación promedio: {puntuacion_promedio:.2f}")

        # Matriz de puntuaciones
        if self.matriz_puntuaciones is not None:
            print("")
            print(f"Matriz de puntuaciones {self.matriz_puntuaciones.shape}:")
            nombres_de_pelicula = [self.peliculas[id]["nombre"][:6] for id in self.ids_peliculas]
            tabla_matriz_puntuaciones = PrettyTable([""] + nombres_de_pelicula)
            for i, id_usuario in enumerate(self.ids_usuarios):
                nombre_usuario = self.usuarios[id_usuario].obtener_nombre()[:6]
                puntuaciones_usuario = [f"{p:8.1f}" for p in self.matriz_puntuaciones[i]]
                tabla_matriz_puntuaciones.add_row([nombre_usuario] + puntuaciones_usuario)
            print(tabla_matriz_puntuaciones)

        # Matriz de similitud
        if self.matriz_similitud_usuarios is not None:
            print("")
            print(f"Matriz de similitud entre usuarios {self.matriz_similitud_usuarios.shape}:")
            nombres_de_usuario = [self.usuarios[id].obtener_nombre() for id in self.ids_usuarios]
            tabla_matriz_similitud = PrettyTable([""] + nombres_de_usuario)
            for i, id_usuario in enumerate(self.ids_usuarios):
                nombre_usuario = self.usuarios[id_usuario].obtener_nombre()
                similitudes = [f"{s:8.3f}" for s in self.matriz_similitud_usuarios[i]]
                tabla_matriz_similitud.add_row([nombre_usuario] + similitudes)
            print(tabla_matriz_similitud)
