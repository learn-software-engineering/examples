from collections import Counter, defaultdict
from datetime import datetime
import json
import os
from typing import Any, Dict, List, Tuple


from configuracion import Configuracion


class SistemaRecomendaciones:
    """
    Este sistema implementa un enfoque híbrido que combina:
      1- Filtrado Colaborativo: Encuentra usuarios similares
      2- Filtrado por Contenido: Analiza características del producto vs perfil usuario
      3- Reglas de Negocio: Aplica lógica específica del dominio
      4- Sistema de Explicaciones: Genera razones comprensibles

    Flujo de datos:
    Usuarios + Productos + Interacciones → Similitudes → Recomendaciones → Explicaciones
    """

    def __init__(self, archivo_config: str = "config.yaml", ruta_datos: str = "datos/"):
        """
        Inicialización del sistema
        Args:
            ruta_datos: Carpeta donde están los archivos JSON con los datos
        ¿Por qué separamos los datos del código?
        - Facilita testing con diferentes datasets
        - Permite actualizar datos sin tocar la lógica
        - Hace el código más mantenible y escalable
        """

        # Configuración
        self.config = Configuracion(archivo_config)

        # Estructuras de datos principales
        self.usuarios: Dict[str, Dict] = {}
        self.productos: Dict[str, Dict] = {}
        self.interacciones: List[Dict] = []
        self.reglas_negocio: List[Dict] = []

        # Configuración del sistema
        self.ruta_datos = ruta_datos

        print("Inicializando Sistema de Recomendaciones")
        self._cargar_datos()
        self._configurar_reglas_negocio()
        print("Sistema listo!")

    def _cargar_datos(self):
        """
        Carga de datos desde archivos externos.
        ¿Por qué usamos archivos JSON?
        - Formato estándar para intercambio de datos
        - Fácil de leer y modificar manualmente
        - Compatible con APIs REST
        - Permite versionado de datos

        Patrón de diseño: Separación de Responsabilidades
        Los datos están separados de la lógica, facilitando mantenimiento
        """
        try:
            # Cargar usuarios
            with open(os.path.join(self.ruta_datos, 'usuarios.json'), 'r', encoding='utf-8') as f:
                datos_usuarios = json.load(f)
                self.usuarios = datos_usuarios['usuarios']
                print(f"   * {len(self.usuarios)} usuarios cargados")

            # Cargar productos
            with open(os.path.join(self.ruta_datos, 'productos.json'), 'r', encoding='utf-8') as f:
                datos_productos = json.load(f)
                self.productos = datos_productos['productos']
                print(f"   * {len(self.productos)} productos cargados")

            # Cargar interacciones
            with open(os.path.join(self.ruta_datos, 'interacciones.json'), 'r', encoding='utf-8') as f:
                datos_interacciones = json.load(f)
                self.interacciones = datos_interacciones['interacciones']
                print(f"   * {len(self.interacciones)} interacciones cargadas")

        except FileNotFoundError as e:
            print(f"Error: No se encontró el archivo {e.filename}")
            print(
                "Asegúrate de tener los archivos usuarios.json, productos.json e interacciones.json")
            raise
        except json.JSONDecodeError as e:
            print(f"Error al leer JSON: {e}")
            raise

    def _configurar_reglas_negocio(self):
        pass

    def _filtrar_por_categoria(self, categoria: str):
        """Helper para crear filtros por categoría"""
        return lambda productos: [p for p in productos if self.productos[p]["categoria"] == categoria]

    def _filtrar_por_precio(self, max_precio: int):
        """Helper para crear filtros por precio"""
        return lambda productos: [p for p in productos if self.productos[p]["precio"] <= max_precio]


    def _calculo_simulitud_por_productos(self, usuario_a: str, usuario_b: str) -> float:
        """
        Calculo de similitud por productos entre usuarios
        """
        similitud_productos = 0
        tipos_a_considerar = ["compra", "valoracion", "wishlist"]

        interacciones_a = self.obtener_interacciones_usuario(usuario_a)
        interacciones_b = self.obtener_interacciones_usuario(usuario_b)

        # Extraer productos con interacciones significativas (compra, valoracion)
        productos_a = {i["producto"] for i in interacciones_a if i["tipo"] in tipos_a_considerar}
        productos_b = {i["producto"] for i in interacciones_b if i["tipo"] in tipos_a_considerar}

        if len(productos_a) == 0 and len(productos_b) == 0:
            similitud_productos = 0.0
        else:
            interseccion = len(productos_a.intersection(productos_b))
            union = len(productos_a.union(productos_b))
            similitud_productos = interseccion / union if union > 0 else 0.0

        return similitud_productos

    def _calculo_similitud_demografica(self, datos_usuario_a: str, datos_usuario_b: str) -> float:
        """
        Calculo de similitud demográfica entre usuarios
        Similitud inversamente proporcional a la diferencia
        """
        similitud_demografica = 0.0

        tolerancia_edad = self.config.get_tolerancia_por_edad_similar()
        booster_por_genero = self.config.get_boost_por_mismo_genero()
        booster_por_ubicacion = self.config.get_boost_por_misma_ubicacion()
        no_booster_proportion = 1 - booster_por_genero - booster_por_ubicacion

        diferencia_edad = abs(datos_usuario_a["edad"] - datos_usuario_b["edad"])
        if diferencia_edad <= tolerancia_edad:
            similitud_demografica += no_booster_proportion * (1 - diferencia_edad / tolerancia_edad)

        # Boost en similitud demográfica por mismo género
        if datos_usuario_a["genero"] == datos_usuario_b["genero"]:
            similitud_demografica += booster_por_genero

        # Boost en similitud demográfica por misma ubicación
        if datos_usuario_a["ubicacion"] == datos_usuario_b["ubicacion"]:
            similitud_demografica += booster_por_ubicacion

        return similitud_demografica

    def _calculo_similitud_por_intereses(self, datos_usuario_a: str, datos_usuario_b: str) -> float:
        """
        Calculo de similitud demográfica entre usuarios
        """
        similitud_por_intereses = 0.0

        intereses_a = set(datos_usuario_a["intereses"])
        intereses_b = set(datos_usuario_b["intereses"])

        if len(intereses_a.union(intereses_b)) > 0:
            interseccion_intereses = len(intereses_a.intersection(intereses_b))
            union_intereses = len(intereses_a.union(intereses_b))
            similitud_por_intereses = interseccion_intereses / union_intereses
        else:
            similitud_por_intereses = 0.0

        return similitud_por_intereses

    def _generar_explicacion(self, id_usuario: str, id_producto: str) -> List[str]:
        """
        Generación de explicaciones

        Las explicaciones son cruciales para generar confianza en el sistema.
        Los usuarios necesitan entender POR QUÉ se les recomienda algo.

        Tipos:
          1- Basadas en intereses: "Coincide con tu interés en tecnología"
          2- Demográficas: "Apropiado para tu grupo de edad"
          3- De precio: "Se ajusta a tu presupuesto"
          4- De calidad: "Excelente valoracion (4.8/5)"
          5- Colaborativas: "A usuarios similares también les gustó"
          6- De popularidad: "Producto muy popular"

        Las explicaciones aumentan:
        - Confianza en el sistema
        - Satisfacción del usuario
        - Probabilidad de compra
        - Comprensión del algoritmo

        Args:
            id_usuario: Usuario que recibe la recomendación
            id_producto: Producto recomendado

        Returns:
            Lista de razones
        """

        usuario = self.usuarios[id_usuario]
        producto = self.productos[id_producto]
        razones = []

        # 1- Basadas en intereses: "Coincide con tu interés en tecnología"
        intereses_usuario = set(usuario["intereses"])
        etiquetas_producto = set(producto.get("etiquetas", []))
        intereses_coinciden = intereses_usuario.intersection(etiquetas_producto)
        if intereses_coinciden:
            if len(intereses_coinciden) == 1:
                razones.append(f"Coincide con tu interés en {list(intereses_coinciden)[0]}")
            else:
                razones.append(f"Coincide con tus intereses: {', '.join(sorted(intereses_coinciden))}")
        if producto["categoria"] in intereses_usuario:
            razones.append(f"Te gusta la categoría {producto['categoria']}")

        # 2- Demográficas: "Apropiado para tu grupo de edad"
        if producto.get("edades_apropiadas"):
            edad_min, edad_max = producto["edades_apropiadas"]
            if edad_min <= usuario["edad"] <= edad_max:
                razones.append("Apropiado para tu grupo de edad")

        # 3- De precio: "Se ajusta a tu presupuesto"
        precio = producto["precio"]
        nivel_gasto = usuario["nivel_gasto"]
        nivel_gasto_alto_precio_min = self.config.get_peso_puntuacion_precio_minimo_para_nivel_gasto_alto()
        nivel_gasto_bajo_precio_max = self.config.get_peso_puntuacion_peso_maximo_para_nivel_de_gasto_bajo()
        if nivel_gasto == "alto" and precio >= nivel_gasto_alto_precio_min:
            razones.append("Producto premium que se ajusta a tu perfil")
        elif nivel_gasto == "medio" and nivel_gasto_bajo_precio_max * 0.65 <= precio <= nivel_gasto_alto_precio_min * 2:
            razones.append("Precio equilibrado para tu rango")
        elif nivel_gasto == "bajo" and precio <= nivel_gasto_bajo_precio_max:
            razones.append("Precio económico y accesible")

        # 4- De calidad: "Excelente valoracion (4.8/5)"
        valoracion = producto.get("valoracion", 0)
        if valoracion >= 4.5:
            razones.append(f"Excelente valoración ({valoracion}/5)")
        elif valoracion >= 4.0:
            razones.append(f"Buena valoración ({valoracion}/5)")

        # 5- Colaborativas: "A usuarios similares también les gustó"
        usuarios_similares = self.encontrar_usuarios_similares(id_usuario, 3)
        for otro_usuario, similitud in usuarios_similares:
            # TODO
            if similitud > 0.3:
                interacciones_otro = self.obtener_interacciones_usuario(otro_usuario)
                productos_otro = [i["producto"] for i in interacciones_otro if i["tipo"] in ["compra", "valoracion"]]
                if id_producto in productos_otro:
                    razones.append("A usuarios con perfil similar también les gustó")
                    break

        # 6- De popularidad: "Producto muy popular"
        popularidad = producto.get("popularidad", 0)
        if popularidad >= 80:
            razones.append("Producto muy popular")

        # Razón por defecto
        if not razones:
            razones.append("Seleccionado especialmente para ti")

        return razones

    def analizar_sistema(self) -> Dict[str, Any]:
        """
        Análisis y estadísticas del sistema

        Proporciona datos sobre el rendimiento y características del sistema.
        Útil para depuración, optimización y reportes.

        Returns:
            Diccionario con estadísticas completas del sistema
        """
        print("\nAnalizando sistema")

        # Estadísticas básicas
        estadisticas = {
            "usuarios": {
                "total": len(self.usuarios),
                "por_genero": Counter([u["genero"] for u in self.usuarios.values()]),
                "por_ubicacion": Counter([u["ubicacion"] for u in self.usuarios.values()]),
                "por_nivel_gasto": Counter([u["nivel_gasto"] for u in self.usuarios.values()]),
                "edad_promedio": sum([u["edad"] for u in self.usuarios.values()]) / len(self.usuarios)
            },
            "productos": {
                "total": len(self.productos),
                "por_categoria": Counter([p["categoria"] for p in self.productos.values()]),
                "precio_promedio": sum([p["precio"] for p in self.productos.values()]) / len(self.productos),
                "valoracion_promedio": sum([p["valoracion"] for p in self.productos.values()]) / len(self.productos)
            },
            "interacciones": {
                "total": len(self.interacciones),
                "por_tipo": Counter([i["tipo"] for i in self.interacciones]),
                "por_usuario": Counter([i["usuario"] for i in self.interacciones]),
                "usuarios_activos": len(set([i["usuario"] for i in self.interacciones]))
            }
        }

        # Análisis de similitudes
        lista_usuarios = list(self.usuarios.keys())
        similitudes = []

        for index_i, primer_usuario in enumerate(lista_usuarios):
            for index_j in range(index_i + 1, len(lista_usuarios)):
                sim = self.calcular_similitud_usuarios(primer_usuario, lista_usuarios[index_j])
                similitudes.append(sim)

        if similitudes:
            estadisticas["similitudes"] = {
                "promedio": sum(similitudes) / len(similitudes),
                "maxima": max(similitudes),
                "minima": min(similitudes)
            }

        return estadisticas

    def calcular_similitud_usuarios(self, usuario_a: str, usuario_b: str) -> float:
        """
        CÁLCULO DE SIMILITUD ENTRE USUARIOS
        Este es el corazón del filtrado colaborativo. Combinamos múltiples métricas
        para determinar qué tan similares son dos usuarios:

        1- Similitud por productos (Índice de Jaccard):
           - Mide productos en común vs total de productos únicos
           - Jaccard = |intersección| / |unión|
           - Rango: 0 (nada en común) a 1 (productos idénticos)
        2- Similitud demográfica
        3- Similitud por intereses:
           - Índice de Jaccard sobre conjunto de intereses
           - Importante para usuarios nuevos sin historial

        Fórmula final:
        Similitud = 0.5 sim_productos + 0.3 sim_demográfica + 0.2 sim_intereses

        ¿Por qué estos pesos?
        - 50% productos: El comportamiento real es lo más importante
        - 30% demografía: Indicador fuerte pero no determinante
        - 20% intereses: Útil para cold start y diversidad
        """

        datos_usuario_a = self.usuarios[usuario_a]
        datos_usuario_b = self.usuarios[usuario_b]

        # Similitud por productos (Jaccard Similarity)
        peso_similitud_por_productos = self.config.get_peso_similitud_por_productos()
        similitud_productos = self._calculo_simulitud_por_productos(usuario_a, usuario_b)

        # Similitud demográgica
        peso_similitud_demografica = self.config.get_peso_similitud_demografica()
        similitud_demografica = self._calculo_similitud_demografica(datos_usuario_a, datos_usuario_b)

        # Similitud por intereses (Jaccard)
        peso_similitud_por_intereses = self.config.get_peso_similitud_por_intereses()
        similitud_por_intereses = self._calculo_similitud_por_intereses(datos_usuario_a, datos_usuario_b)

        # Combinación final con pesos
        similitud_total = (
            peso_similitud_por_productos * similitud_productos +
            peso_similitud_demografica * similitud_demografica +
            peso_similitud_por_intereses * similitud_por_intereses
        )

        return similitud_total

    def encontrar_usuarios_similares(self, id_usuario: str, n: int = 3) -> List[Tuple[str, float]]:
        """
        Búsqueda de usuario similares

        Encuentra los N usuarios más similares al usuario objetivo.
        Esta es la base del filtrado colaborativo.

        Procedimiento:
        1. Calcula similitud con todos los demás usuarios
        2. Ordena por similitud descendente
        3. Retorna los primeros N

        Optimizaciones posibles:
          - Para tiempo real: pre-calcular similitudes offline
          - Para escalabilidad: usar algoritmos aproximados

        Args:
            id_usuario: Usuario objetivo
            n: Número de usuarios similares a retornar

        Returns:
            Lista de tuplas (id_usuario, similitud) ordenada por similitud
        """

        if id_usuario not in self.usuarios:
            raise ValueError(f"Usuario {id_usuario} no existe")

        similitudes = []

        # Calcular similitud con todos los demás usuarios
        for otro_usuario in self.usuarios:
            if otro_usuario != id_usuario:
                sim = self.calcular_similitud_usuarios(id_usuario, otro_usuario)
                similitudes.append((otro_usuario, sim))

        # Ordenar por similitud descendente
        similitudes.sort(key=lambda x: x[1], reverse=True)

        return similitudes[:n]

    def generar_recomendaciones(self, id_usuario: str, n: int = 5, incluir_explicacion: bool = True) -> Dict[str, Any]:
        """
        Generación de recomendaciones

        Esta es la función principal que orquesta todo el sistema.
        Combina múltiples estrategias para generar recomendaciones híbridas.

        Proceso completo:
          1- Validación de entrada
          2- Recomendaciones colaborativas (usuarios similares)
          3- Recomendaciones por contenido (perfil del usuario)
          4- Combinación híbrida con pesos
          5- Aplicación de reglas de negocio
          6- Selección de top N
          7- Enriquecimiento con datos del usuario y del producto
          8- Generación de explicaciones

        Estrategia de combinación:
        - Porcentaje de filtrado colaborativo: Aprovecha la "sabiduría de las masas"
        - Porcentaje de filtrado por contenido: Asegura relevancia con el perfil

        ¿Por qué estos pesos?
        - El comportamiento real (colaborativo) es más predictivo
        - El contenido asegura relevancia y diversidad
        - Balance entre exploración y explotación

        Args:
            id_usuario: Usuario objetivo
            n: Número de recomendaciones a generar
            incluir_explicacion: Si generar explicaciones

        Returns:
            Diccionario con recomendaciones completas y metadatos
        """

        # 1- Validación
        if id_usuario not in self.usuarios:
            return {"error": f"Usuario {id_usuario} no encontrado"}

        usuario_nombre = self.usuarios[id_usuario]['nombre']
        message = f"Generando recomendaciones para {usuario_nombre}"
        print(message)
        print("=" * len(message))

        # 2- Recomendaciones colaborativas
        rec_colaborativo = self.recomendar_por_filtrado_colaborativo(id_usuario, n*3)

        # 3-  Recomendaciones por contenido
        rec_contenido = self.recomendar_por_contenido(id_usuario, n*3)

        # 4- Combinación
        print(f"   Combinando estrategias de recomendación")
        pesos_algoritmos = self.config.get_pesos_algoritmos()
        puntuaciones_combinados = defaultdict(float)
        peso_colaborativo = pesos_algoritmos["filtrado_colaborativo"]
        peso_contenido = pesos_algoritmos["filtrado_contenido"]
        for producto, puntuacion in rec_colaborativo:
            puntuaciones_combinados[producto] += peso_colaborativo * puntuacion
        for producto, puntuacion in rec_contenido:
            puntuaciones_combinados[producto] += peso_contenido * puntuacion

        print(f"      * Productos únicos después de combinar: {len(puntuaciones_combinados)}")

        # TODO
        # 5- Aplicación de reglas de negocio
        recomendaciones_raw = list(puntuaciones_combinados.items())
        recomendaciones_ajustadas = recomendaciones_raw
        # recomendaciones_ajustadas = self.aplicar_reglas_negocio(usuario_id, recomendaciones_raw)

        # Seleccionar las primeras N recomendaciones
        primeras_recomendaciones = recomendaciones_ajustadas[:n]

        print(f"   Primeras {len(primeras_recomendaciones)} recomendaciones seleccionadas")

        # Enriquecimiento con datos del usuario y del producto
        resultado = {
            "usuario": usuario_nombre,
            "usuario_id": id_usuario,
            "total_recomendaciones": len(primeras_recomendaciones),
            "algoritmo": "Híbrido (Colaborativo + Contenido + Reglas)",
            "pesos": {
                "colaborativo": peso_colaborativo,
                "contenido": peso_contenido
            },
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "productos": []
        }

        # Generación de explicaciones
        for i, (id_producto, puntuacion) in enumerate(primeras_recomendaciones, 1):
            producto = self.productos[id_producto]

            item = {
                "ranking": i,
                "id": id_producto,
                "nombre": producto["nombre"],
                "categoria": producto["categoria"],
                "precio": producto["precio"],
                "precio_formateado": f"${producto['precio']:,}",
                "valoracion": producto["valoracion"],
                "popularidad": producto.get("popularidad", 0),
                "puntuacion": round(puntuacion, 3),
                "etiquetas": producto.get("etiquetas", [])
            }

            if incluir_explicacion:
                item["explicacion"] = self._generar_explicacion(id_usuario, id_producto)
                item["texto_explicacion"] = "; ".join(item["explicacion"])

            resultado["productos"].append(item)

        print(f"   Recomendaciones generadas exitosamente!")
        return resultado

    def imprimir_reporte_detallado(self, id_usuario: str):
        """
        Reporte detallado para un usuario

        Genera un reporte completo mostrando cómo funciona el sistema
        para un usuario específico. Útil para debugging y educación.

        Args:
            id_usuario: Usuario para generar el reporte
        """

        if id_usuario not in self.usuarios:
            print(f"Usuario {id_usuario} no encontrado")
            return

        usuario = self.usuarios[id_usuario]

        message = f"Reporte Detallado - {usuario['nombre'].upper()}"
        print("\n")
        print("=" * len(message))
        print(message)
        print("=" * len(message))

        # Información del usuario
        print("Perfil del usuario")
        print(f"   * Edad: {usuario['edad']} años")
        print(f"   * Género: {usuario['genero']}")
        print(f"   * Ubicación: {usuario['ubicacion']}")
        print(f"   * Intereses: {', '.join(usuario['intereses'])}")
        print(f"   * Nivel de gasto: {usuario['nivel_gasto']}")

        # Historial de interacciones
        interacciones = self.obtener_interacciones_usuario(id_usuario)
        print(f"Historial de actividad ({len(interacciones)} interacciones):")

        for interaccion in interacciones[-5:]:  # Últimas 5
            producto = self.productos[interaccion['producto']]
            valoracion_str = f" (Calificación: {interaccion['valoracion']}/5)" if interaccion['valoracion'] else ""
            print(f"   • {interaccion['fecha']}: {interaccion['tipo'].upper()} - {producto['nombre']}{valoracion_str}")

        # Usuarios similares
        cantidad_usuarios_similares = 3
        usuarios_similares = self.encontrar_usuarios_similares(id_usuario, cantidad_usuarios_similares)
        print(f"{cantidad_usuarios_similares} usuarios más similares")

        for otro_usuario, similitud in usuarios_similares:
            otro_nombre = self.usuarios[otro_usuario]['nombre']
            print(f"   * {otro_nombre}: {similitud:.3f} ({similitud*100:.1f}% similar)")

        # Recomendaciones
        cantidad_recomendaciones = 5
        recomendaciones = self.generar_recomendaciones(id_usuario, n=cantidad_recomendaciones)
        print(f"{cantidad_recomendaciones} recomendaciones generadas:")

        for producto in recomendaciones['productos']:
            print(f"   #{producto['ranking']} - {producto['nombre']}")
            print(f"      Precio: {producto['precio_formateado']}")
            print(f"      Calificación: {producto['valoracion']}/5")
            print(f"      Puntuación: {producto['puntuacion']}")
            if "texto_explicacion" in producto:
                print(f"      Explicación: {producto['texto_explicacion']}")

    def obtener_interacciones_usuario(self, id_usuario: str) -> List[Dict]:
        """
        Extracción del historial del usuario
        Esta función es fundamental para el filtrado colaborativo.
        Obtiene todas las interacciones (compras, views, valoraciones) de un usuario.
        ¿Por qué es importante?
        - Base para calcular similitudes entre usuarios
        - Evita recomendar productos ya conocidos
        - Permite ponderar por tipo de interacción

        Args:
            id_usuario: ID del usuario

        Returns:
            Lista de interacciones del usuario ordenadas por fecha
        """
        interacciones_usuario = [
            interaccion for interaccion in self.interacciones
            if interaccion["usuario"] == id_usuario
        ]

        # Ordenar por fecha (más recientes primero)
        interacciones_usuario.sort(
            key=lambda x: datetime.strptime(x["fecha"], "%Y-%m-%d"),
            reverse=True
        )

        return interacciones_usuario

    def recomendar_por_contenido(self, id_usuario: str, n: int = 5) -> List[Tuple[str, float]]:
        """
        Recomendaciones basadas en contenido

        Analiza las características del usuario vs características de productos
        para encontrar matches relevantes.

        Factores de puntuacion:
          Compatibilidad de intereses:
            - Interés coincide con categoría del producto
            - Interés coincide con etiquetas del producto
          Compatibilidad demográfica:
            - Edad del usuario dentro del rango objetivo del producto
          Calidad del producto
            - Valoración promedio normalizada (0-1)
          Popularidad general
            - Popularidad normalizada (0-1)
          Adecuación del precio:
            - Precio apropiado para el nivel de gasto del usuario

        Ventajas:
        - Funciona bien para usuarios/productos nuevos
        - Explicable y transparente
        - No requiere datos de otros usuarios

        Limitaciones:
        - Puede ser repetitivo (más de lo mismo)
        - Requiere buenos metadatos de productos
        - Dificulta el descubrimiento serendípico
        """
        print(f"   Aplicando filtrado por contenido para {self.usuarios[id_usuario]['nombre']}...")

        usuario = self.usuarios[id_usuario]
        puntuaciones = {}

        for id_producto, producto in self.productos.items():
            puntuacion = 0.0

            # Compatibilidad de intereses
            intereses_usuario = set(usuario["intereses"])

            categoria_producto = producto["categoria"]
            if categoria_producto in intereses_usuario:
                puntuacion += self.config.get_peso_puntuacion_interes_categoria()

            etiquetas_producto = set(producto.get("etiquetas", []))
            coincidencias_etiquetas = intereses_usuario.intersection(etiquetas_producto)
            puntuacion += len(coincidencias_etiquetas) * self.config.get_peso_puntuacion_interes_etiquetas()

            # Compatibilidad demográfica
            edad_usuario = usuario["edad"]
            if producto.get("edades_apropiadas"):
                edad_min, edad_max = producto["edades_apropiadas"]
                if edad_min <= edad_usuario <= edad_max:
                    puntuacion += self.config.get_peso_puntuacion_edad_apropiada()
                elif abs(edad_usuario - edad_min) <= 5 or abs(edad_usuario - edad_max) <= 5:
                    puntuacion += 0.75  # Tolerancia de ±5 años

            # Calidad del producto
            valoracion = producto.get("valoracion", 0)
            puntuacion += valoracion / 5.0  # Normalizar 0-5 → 0-1

            # Popularidad general
            popularidad = producto.get("popularidad", 0)
            puntuacion += popularidad / 100.0  # Normalizar 0-100 → 0-1

            # Adecuación del precio
            precio = producto["precio"]
            nivel_gasto = usuario["nivel_gasto"]
            nivel_gasto_alto_precio_min = self.config.get_peso_puntuacion_precio_minimo_para_nivel_gasto_alto()
            nivel_gasto_bajo_precio_max = self.config.get_peso_puntuacion_peso_maximo_para_nivel_de_gasto_bajo()
            peso_precio_apropiado = self.config.get_peso_puntuacion_precio_apropiado()
            if nivel_gasto == "alto" and precio >= nivel_gasto_alto_precio_min:
                puntuacion += peso_precio_apropiado
            elif nivel_gasto == "medio" and nivel_gasto_bajo_precio_max * 0.65 <= precio <= nivel_gasto_alto_precio_min * 2:
                puntuacion += peso_precio_apropiado
            elif nivel_gasto == "bajo" and precio <= nivel_gasto_bajo_precio_max:
                puntuacion += peso_precio_apropiado
            else:
                # Penalizar ligeramente si el precio no es apropiado
                puntuacion -= self.config.get_peso_puntuacion_penalizacion_precio()

            puntuaciones[id_producto] = puntuacion

        # Filtrar productos ya conocidos
        interacciones_usuario = self.obtener_interacciones_usuario(id_usuario)
        productos_conocidos = {i["producto"] for i in interacciones_usuario}

        # Generar recomendaciones finales
        recomendaciones = [
            (producto, puntuacion) for producto, puntuacion in puntuaciones.items()
            if producto not in productos_conocidos and puntuacion > 0
        ]
        recomendaciones.sort(key=lambda x: x[1], reverse=True)
        print(f"   {len(recomendaciones[:n])} recomendaciones por contenido generadas")

        return recomendaciones[:n]

    def recomendar_por_filtrado_colaborativo(self, id_usuario: str, n: int = 5) -> List[Tuple[str, float]]:
        """
        Recomendaciones por filtrado colaborativo

        Implementa el algoritmo clásico: "A usuarios como tú también les gustó..."

        Algoritmo:
        1- Encuentra usuarios similares al objetivo
        2- Recopila productos que compraron/valoraron positivamente, pondera por: similitud_usuario * valoracion_producto
        3- Filtra productos ya conocidos por el usuario
        4- Ordena por puntuación y retorna primeros N

        Ventajas:
        - Descubre productos inesperados
        - Funciona bien con usuarios activos
        - Captura preferencias implícitas

        Limitaciones:
        - Cold start problem (usuarios/productos nuevos)
        - Sparsity problem (pocos datos)
        - Popular bias (favorece productos populares)

        Args:
            id_usuario: Usuario para quien generar recomendaciones
            n: Número máximo de recomendaciones

        Returns:
            Lista de (id_produto, puntuacion) ordenada por puntuacion descendente
        """

        print(f"   Aplicando filtrado colaborativo para {self.usuarios[id_usuario]['nombre']}...")

        # Encuentra usuarios similares al objetivo
        usuarios_similares = self.encontrar_usuarios_similares(id_usuario, n=5)

        if not usuarios_similares:
            print("   No se encontraron usuarios similares")
            return []

        print(f"   Usuarios similares encontrados: {len(usuarios_similares)}")

        # Recopila productos que compraron/valoraron positivamente
        productos_candidatos = Counter()

        for usuario_similar, similitud in usuarios_similares:
            # Solo considerar interacciones fuertes (no solo views)
            interacciones = [
                i for i in self.obtener_interacciones_usuario(usuario_similar)
                if i["tipo"] in ["compra", "valoracion"] and i.get("valoracion", 0) >= 3
            ]

            for interaccion in interacciones:
                producto = interaccion["producto"]

                # Calcular puntuación: similitud * (valoracion normalizado)
                puntuacion = similitud
                if interaccion.get("valoracion"):
                    puntuacion *= (interaccion["valoracion"] / 5.0)  # Normalizar 1-5 → 0.2-1.0
                else:
                    puntuacion *= 0.8  # Puntuación por defecto para compras sin valoracion

                productos_candidatos[producto] += puntuacion

        # 3- Filtra productos ya conocidos por el usuario
        interacciones_usuario = self.obtener_interacciones_usuario(id_usuario)
        productos_conocidos = set(i["producto"] for i in interacciones_usuario)

        # 4- Ordena por puntuación y retorna primeros N
        recomendaciones = [
            (producto, puntuacion) for producto, puntuacion in productos_candidatos.items()
            if producto not in productos_conocidos
        ]
        recomendaciones.sort(key=lambda x: x[1], reverse=True)

        print(f"   {len(recomendaciones[:n])} recomendaciones colaborativas generadas")

        return recomendaciones[:n]
