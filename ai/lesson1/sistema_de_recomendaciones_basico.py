import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import random

class SistemaRecomendaciones:
    """
    Sistema de recomendaciones basado en reglas lógicas y filtrado colaborativo básico.

    Combina múltiples estrategias:
    1. Recomendaciones por perfil (demografía, preferencias)
    2. Filtrado colaborativo simple (usuarios similares)
    3. Recomendaciones por contenido (características del producto)
    4. Reglas de negocio (promociones, estacionalidad, etc.)
    """

    def __init__(self):
        # Base de datos simulada
        self.usuarios = {}
        self.productos = {}
        self.interacciones = []  # historial de compras/views/ratings
        self.reglas_negocio = []

        # Inicializar con datos de ejemplo
        self._cargar_datos_ejemplo()
        self._configurar_reglas_negocio()

    def _cargar_datos_ejemplo(self):
        """Crea datos de ejemplo para probar el sistema"""

        # Usuarios de ejemplo con diferentes perfiles
        self.usuarios = {
            "user_001": {
                "nombre": "Ana López",
                "edad": 28,
                "genero": "F",
                "ubicacion": "Buenos Aires",
                "intereses": ["tecnologia", "fitness", "lectura"],
                "nivel_gasto": "medio"
            },
            "user_002": {
                "nombre": "Carlos Mendez",
                "edad": 35,
                "genero": "M",
                "ubicacion": "Córdoba",
                "intereses": ["deportes", "gaming", "musica"],
                "nivel_gasto": "alto"
            },
            "user_003": {
                "nombre": "María Rodriguez",
                "edad": 42,
                "genero": "F",
                "ubicacion": "Rosario",
                "intereses": ["cocina", "jardineria", "arte"],
                "nivel_gasto": "bajo"
            },
            "user_004": {
                "nombre": "Diego Silva",
                "edad": 24,
                "genero": "M",
                "ubicacion": "Buenos Aires",
                "intereses": ["tecnologia", "gaming", "fitness"],
                "nivel_gasto": "medio"
            }
        }

        # Catálogo de productos
        self.productos = {
            "prod_001": {
                "nombre": "Smartphone Samsung Galaxy",
                "categoria": "tecnologia",
                "precio": 150000,
                "rating": 4.5,
                "tags": ["android", "camara", "5g"],
                "target_edad": [20, 50],
                "popularidad": 95
            },
            "prod_002": {
                "nombre": "Auriculares Bluetooth Sport",
                "categoria": "tecnologia",
                "precio": 25000,
                "rating": 4.2,
                "tags": ["bluetooth", "deportes", "resistente"],
                "target_edad": [18, 40],
                "popularidad": 80
            },
            "prod_003": {
                "nombre": "Libro: Cocina Mediterránea",
                "categoria": "lectura",
                "precio": 3500,
                "rating": 4.8,
                "tags": ["cocina", "recetas", "salud"],
                "target_edad": [25, 65],
                "popularidad": 60
            },
            "prod_004": {
                "nombre": "Juego: Call of Duty",
                "categoria": "gaming",
                "precio": 12000,
                "rating": 4.3,
                "tags": ["accion", "multijugador", "fps"],
                "target_edad": [16, 35],
                "popularidad": 90
            },
            "prod_005": {
                "nombre": "Kit Herramientas Jardín",
                "categoria": "hogar",
                "precio": 8500,
                "rating": 4.0,
                "tags": ["jardineria", "herramientas", "exterior"],
                "target_edad": [30, 70],
                "popularidad": 45
            }
        }

        # Historial de interacciones (simulado)
        self.interacciones = [
            {"usuario": "user_001", "producto": "prod_001", "tipo": "compra", "rating": 5, "fecha": "2024-08-01"},
            {"usuario": "user_001", "producto": "prod_002", "tipo": "view", "rating": None, "fecha": "2024-08-05"},
            {"usuario": "user_002", "producto": "prod_004", "tipo": "compra", "rating": 4, "fecha": "2024-08-03"},
            {"usuario": "user_002", "producto": "prod_001", "tipo": "view", "rating": None, "fecha": "2024-08-07"},
            {"usuario": "user_003", "producto": "prod_003", "tipo": "compra", "rating": 5, "fecha": "2024-08-02"},
            {"usuario": "user_003", "producto": "prod_005", "tipo": "view", "rating": None, "fecha": "2024-08-06"},
            {"usuario": "user_004", "producto": "prod_002", "tipo": "compra", "rating": 4, "fecha": "2024-08-04"},
            {"usuario": "user_004", "producto": "prod_004", "tipo": "view", "rating": None, "fecha": "2024-08-08"}
        ]

    def _configurar_reglas_negocio(self):
        """Define reglas de negocio específicas del dominio"""

        self.reglas_negocio = [
            {
                "nombre": "boost_tecnologia_jovenes",
                "condicion": lambda user: user["edad"] < 35,
                "accion": lambda productos: [p for p in productos if self.productos[p]["categoria"] == "tecnologia"],
                "boost": 1.3,
                "descripcion": "Usuarios jóvenes prefieren tecnología"
            },
            {
                "nombre": "descuento_nivel_gasto_alto",
                "condicion": lambda user: user["nivel_gasto"] == "alto",
                "accion": lambda productos: productos,  # aplica a todos
                "boost": 1.2,
                "descripcion": "Usuarios con alto gasto ven más productos premium"
            },
            {
                "nombre": "productos_economicos_gasto_bajo",
                "condicion": lambda user: user["nivel_gasto"] == "bajo",
                "accion": lambda productos: [p for p in productos if self.productos[p]["precio"] < 10000],
                "boost": 1.4,
                "descripcion": "Usuarios con gasto bajo ven productos económicos"
            },
            {
                "nombre": "misma_ubicacion_boost",
                "condicion": lambda user: True,  # aplica a todos
                "accion": self._productos_ubicacion_similar,
                "boost": 1.1,
                "descripcion": "Boost para productos populares en la misma región"
            }
        ]

    def _productos_ubicacion_similar(self, productos):
        """
        Simula boost para productos populares en la misma ubicación.
        En un sistema real, esto vendría de analytics.
        """
        # Para simplicidad, asumimos que algunos productos son más populares en ciertas regiones
        productos_regionales = {
            "Buenos Aires": ["prod_001", "prod_002", "prod_004"],  # tech y gaming
            "Córdoba": ["prod_003", "prod_005"],  # hogar y lectura
            "Rosario": ["prod_003", "prod_005"]   # hogar y lectura
        }

        # En un caso real, filtraríamos por la ubicación del usuario actual
        # Aquí simplemente devolvemos todos para mantener simplicidad
        return productos

    def obtener_interacciones_usuario(self, usuario_id):
        """Obtiene el historial de interacciones de un usuario específico"""
        return [i for i in self.interacciones if i["usuario"] == usuario_id]

    def calcular_similitud_usuarios(self, usuario_a, usuario_b):
        """
        Calcula similitud entre dos usuarios basándose en:
        1. Productos en común que han interactuado
        2. Similitud demográfica
        3. Intereses compartidos
        """

        # Obtener interacciones de ambos usuarios
        inter_a = self.obtener_interacciones_usuario(usuario_a)
        inter_b = self.obtener_interacciones_usuario(usuario_b)

        productos_a = set([i["producto"] for i in inter_a])
        productos_b = set([i["producto"] for i in inter_b])

        # 1. Similitud por productos (Jaccard)
        if len(productos_a) == 0 and len(productos_b) == 0:
            sim_productos = 0
        else:
            interseccion = len(productos_a.intersection(productos_b))
            union = len(productos_a.union(productos_b))
            sim_productos = interseccion / union if union > 0 else 0

        # 2. Similitud demográfica
        user_a_data = self.usuarios[usuario_a]
        user_b_data = self.usuarios[usuario_b]

        sim_demografica = 0

        # Edad similar (+/- 10 años)
        diff_edad = abs(user_a_data["edad"] - user_b_data["edad"])
        if diff_edad <= 10:
            sim_demografica += 0.3

        # Mismo género
        if user_a_data["genero"] == user_b_data["genero"]:
            sim_demografica += 0.2

        # Misma ubicación
        if user_a_data["ubicacion"] == user_b_data["ubicacion"]:
            sim_demografica += 0.2

        # 3. Intereses compartidos
        intereses_a = set(user_a_data["intereses"])
        intereses_b = set(user_b_data["intereses"])

        if len(intereses_a.union(intereses_b)) > 0:
            sim_intereses = len(intereses_a.intersection(intereses_b)) / len(intereses_a.union(intereses_b))
        else:
            sim_intereses = 0

        # Combinamos las similitudes con pesos
        similitud_total = (
            0.4 * sim_productos +      # 40% peso a productos compartidos
            0.3 * sim_demografica +    # 30% peso a demografía
            0.3 * sim_intereses        # 30% peso a intereses
        )

        return similitud_total

    def encontrar_usuarios_similares(self, usuario_id, n=3):
        """Encuentra los N usuarios más similares al usuario dado"""

        similitudes = []

        for otro_usuario in self.usuarios:
            if otro_usuario != usuario_id:
                sim = self.calcular_similitud_usuarios(usuario_id, otro_usuario)
                similitudes.append((otro_usuario, sim))

        # Ordenar por similitud descendente
        similitudes.sort(key=lambda x: x[1], reverse=True)

        return similitudes[:n]

    def recomendar_por_filtrado_colaborativo(self, usuario_id, n=5):
        """
        Recomendaciones basadas en usuarios similares.
        "A los usuarios como tú también les gustó..."
        """

        # Encontrar usuarios similares
        usuarios_similares = self.encontrar_usuarios_similares(usuario_id)

        # Obtener productos que interactuaron usuarios similares
        productos_recomendados = Counter()

        for usuario_similar, similitud in usuarios_similares:
            interacciones = self.obtener_interacciones_usuario(usuario_similar)

            for interaccion in interacciones:
                if interaccion["tipo"] in ["compra", "rating"]:  # solo interacciones fuertes
                    # Puntuamos por similitud del usuario y rating si existe
                    score = similitud
                    if interaccion["rating"]:
                        score *= (interaccion["rating"] / 5.0)  # normalizar rating

                    productos_recomendados[interaccion["producto"]] += score

        # Filtrar productos que el usuario ya interactuó
        interacciones_usuario = self.obtener_interacciones_usuario(usuario_id)
        productos_ya_vistos = set([i["producto"] for i in interacciones_usuario])

        # Filtrar y ordenar
        recomendaciones_filtradas = [
            (prod, score) for prod, score in productos_recomendados.items()
            if prod not in productos_ya_vistos
        ]

        recomendaciones_filtradas.sort(key=lambda x: x[1], reverse=True)

        return recomendaciones_filtradas[:n]

    def recomendar_por_contenido(self, usuario_id, n=5):
        """
        Recomendaciones basadas en las características del usuario.
        "Esto podría gustarte basándose en tu perfil..."
        """

        usuario = self.usuarios[usuario_id]
        scores = {}

        for producto_id, producto in self.productos.items():
            score = 0

            # 1. Matching por intereses
            for interes in usuario["intereses"]:
                if interes in producto.get("tags", []) or interes == producto["categoria"]:
                    score += 2

            # 2. Matching por rango de edad
            edad_usuario = usuario["edad"]
            if producto.get("target_edad"):
                edad_min, edad_max = producto["target_edad"]
                if edad_min <= edad_usuario <= edad_max:
                    score += 1.5

            # 3. Rating del producto (calidad)
            score += producto["rating"] / 5.0

            # 4. Popularidad general
            score += producto["popularidad"] / 100.0

            # 5. Precio apropiado para el nivel de gasto
            if usuario["nivel_gasto"] == "alto" and producto["precio"] > 50000:
                score += 1
            elif usuario["nivel_gasto"] == "medio" and 10000 <= producto["precio"] <= 50000:
                score += 1
            elif usuario["nivel_gasto"] == "bajo" and producto["precio"] < 10000:
                score += 1

            scores[producto_id] = score

        # Filtrar productos ya vistos
        interacciones_usuario = self.obtener_interacciones_usuario(usuario_id)
        productos_ya_vistos = set([i["producto"] for i in interacciones_usuario])

        recomendaciones_filtradas = [
            (prod, score) for prod, score in scores.items()
            if prod not in productos_ya_vistos and score > 0
        ]

        recomendaciones_filtradas.sort(key=lambda x: x[1], reverse=True)

        return recomendaciones_filtradas[:n]

    def aplicar_reglas_negocio(self, usuario_id, recomendaciones):
        """
        Aplica reglas de negocio para ajustar las recomendaciones.
        Permite incorporar lógica específica del dominio.
        """

        usuario = self.usuarios[usuario_id]
        recomendaciones_ajustadas = {}

        # Convertir lista de tuplas a diccionario para fácil manipulación
        for prod_id, score in recomendaciones:
            recomendaciones_ajustadas[prod_id] = score

        # Aplicar cada regla de negocio
        for regla in self.reglas_negocio:
            if regla["condicion"](usuario):
                # Obtener productos que aplican para esta regla
                productos_aplicables = regla["accion"](list(recomendaciones_ajustadas.keys()))

                # Aplicar boost
                for producto in productos_aplicables:
                    if producto in recomendaciones_ajustadas:
                        recomendaciones_ajustadas[producto] *= regla["boost"]

        # Convertir de vuelta a lista ordenada
        resultado = [(prod, score) for prod, score in recomendaciones_ajustadas.items()]
        resultado.sort(key=lambda x: x[1], reverse=True)

        return resultado

    def generar_recomendaciones(self, usuario_id, n=5, incluir_explicacion=True):
        """
        Genera recomendaciones finales combinando múltiples estrategias.

        Args:
            usuario_id (str): ID del usuario
            n (int): Número de recomendaciones a generar
            incluir_explicacion (bool): Si incluir explicación de por qué se recomienda

        Returns:
            dict: Recomendaciones con scores y explicaciones
        """

        if usuario_id not in self.usuarios:
            return {"error": f"Usuario {usuario_id} no encontrado"}

        print(f"🎯 Generando recomendaciones para {self.usuarios[usuario_id]['nombre']}...")

        # 1. Recomendaciones por filtrado colaborativo
        rec_colaborativo = self.recomendar_por_filtrado_colaborativo(usuario_id, n*2)
        print(f"   • Filtrado colaborativo: {len(rec_colaborativo)} productos")

        # 2. Recomendaciones por contenido
        rec_contenido = self.recomendar_por_contenido(usuario_id, n*2)
        print(f"   • Basado en contenido: {len(rec_contenido)} productos")

        # 3. Combinar estrategias con pesos
        scores_combinados = defaultdict(float)

        # Peso 60% a filtrado colaborativo, 40% a contenido
        for prod, score in rec_colaborativo:
            scores_combinados[prod] += 0.6 * score

        for prod, score in rec_contenido:
            scores_combinados[prod] += 0.4 * score

        # 4. Aplicar reglas de negocio
        recomendaciones_raw = list(scores_combinados.items())
        recomendaciones_finales = self.aplicar_reglas_negocio(usuario_id, recomendaciones_raw)

        # 5. Tomar top N
        top_recomendaciones = recomendaciones_finales[:n]

        # 6. Agregar información detallada y explicaciones
        resultado = {
            "usuario": self.usuarios[usuario_id]["nombre"],
            "total_recomendaciones": len(top_recomendaciones),
            "productos": []
        }

        for producto_id, score in top_recomendaciones:
            producto = self.productos[producto_id]

            item = {
                "id": producto_id,
                "nombre": producto["nombre"],
                "categoria": producto["categoria"],
                "precio": producto["precio"],
                "rating": producto["rating"],
                "score": round(score, 2)
            }

            if incluir_explicacion:
                item["explicacion"] = self._generar_explicacion(usuario_id, producto_id)

            resultado["productos"].append(item)

        return resultado

    def _generar_explicacion(self, usuario_id, producto_id):
        """
        Genera explicación de por qué se recomienda este producto.
        Ayuda a generar confianza en el sistema.
        """

        usuario = self.usuarios[usuario_id]
        producto = self.productos[producto_id]

        razones = []

        # Razones basadas en intereses
        intereses_match = set(usuario["intereses"]).intersection(set(producto.get("tags", [])))
        if intereses_match:
            razones.append(f"Coincide con tus intereses: {', '.join(intereses_match)}")

        if usuario["intereses"] and producto["categoria"] in usuario["intereses"]:
            razones.append(f"Te gusta la categoría {producto['categoria']}")

        # Razones demográficas
        if producto.get("target_edad"):
            edad_min, edad_max = producto["target_edad"]
            if edad_min <= usuario["edad"] <= edad_max:
                razones.append("Apropiado para tu grupo de edad")

        # Razones de precio
        if usuario["nivel_gasto"] == "alto" and producto["precio"] > 50000:
            razones.append("Producto premium que se ajusta a tu perfil")
        elif usuario["nivel_gasto"] == "medio" and 10000 <= producto["precio"] <= 50000:
            razones.append("Precio equilibrado para tu rango")
        elif usuario["nivel_gasto"] == "bajo" and producto["precio"] < 10000:
            razones.append("Precio económico")

        # Razones de calidad
        if producto["rating"] >= 4.5:
            razones.append(f"Excelente rating ({producto['rating']}/5)")
        elif producto["rating"] >= 4.0:
            razones.append(f"Buena valoración ({producto['rating']}/5)")

        # Razones colaborativas
        usuarios_similares = self.encontrar_usuarios_similares(usuario_id, 3)
        for otro_usuario, similitud in usuarios_similares:
            interacciones_otro = self.obtener_interacciones_usuario(otro_usuario)
            productos_otro = [i["producto"] for i in interacciones_otro if i["tipo"] in ["compra", "rating"]]
            if producto_id in productos_otro:
                razones.append(f"A usuarios con perfil similar también les gustó")
                break

        return razones if razones else ["Recomendado para ti"]


# Ejemplo de uso del sistema completo
if __name__ == "__main__":
    # Crear sistema de recomendaciones
    sistema = SistemaRecomendaciones()

    print("🛍️  SISTEMA DE RECOMENDACIONES INTELIGENTE")
    print("=" * 60)

    # Generar recomendaciones para cada usuario
    for usuario_id in sistema.usuarios.keys():
        print(f"\n{'='*60}")

        recomendaciones = sistema.generar_recomendaciones(usuario_id, n=3, incluir_explicacion=True)

        print(f"\n🎁 RECOMENDACIONES PARA {recomendaciones['usuario'].upper()}")
        print(f"Total: {recomendaciones['total_recomendaciones']} productos")

        for i, producto in enumerate(recomendaciones['productos'], 1):
            print(f"\n#{i} - {producto['nombre']}")
            print(f"    💰 Precio: ${producto['precio']:,}")
            print(f"    ⭐ Rating: {producto['rating']}/5")
            print(f"    🎯 Score: {producto['score']}")
            print(f"    📝 Por qué: {', '.join(producto['explicacion'])}")

    print(f"\n{'='*60}")
    print("🔍 ANÁLISIS DEL SISTEMA:")

    # Mostrar similitudes entre usuarios
    print(f"\n👥 SIMILITUDES ENTRE USUARIOS:")
    usuarios_list = list(sistema.usuarios.keys())

    for i in range(len(usuarios_list)):
        for j in range(i+1, len(usuarios_list)):
            usuario_a = usuarios_list[i]
            usuario_b = usuarios_list[j]

            sim = sistema.calcular_similitud_usuarios(usuario_a, usuario_b)
            nombre_a = sistema.usuarios[usuario_a]["nombre"]
            nombre_b = sistema.usuarios[usuario_b]["nombre"]

            print(f"   {nombre_a} ↔ {nombre_b}: {sim:.2f} ({sim*100:.0f}% similar)")

    # Mostrar estadísticas del catálogo
    print(f"\n📊 ESTADÍSTICAS DEL CATÁLOGO:")
    print(f"   • Total usuarios: {len(sistema.usuarios)}")
    print(f"   • Total productos: {len(sistema.productos)}")
    print(f"   • Total interacciones: {len(sistema.interacciones)}")

    categorias = Counter([p["categoria"] for p in sistema.productos.values()])
    print(f"   • Categorías: {dict(categorias)}")
