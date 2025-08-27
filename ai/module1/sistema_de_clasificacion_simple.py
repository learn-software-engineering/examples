from collections import defaultdict, Counter
import math
import unicodedata


class ClasificadorTextoBasico:
    """
    Clasificador de texto usando probabilidades bayesianas básicas.
    Útil para clasificar emails, reseñas, tickets de soporte, etc.
    """

    def __init__(self):
        # Almacena las frecuencias de palabras por categoría
        self.palabras_por_categoria = defaultdict(Counter)
        # Almacena cuántos tickets hay por categoría
        self.tickets_por_categoria = defaultdict(int)
        # Lista de todas las categorías conocidas
        self.categorias = set()
        # Vocabulario total (todas las palabras únicas)
        self.vocabulario = set()

    def preprocesar_texto(self, texto):
        # Convertir a minúsculas
        texto = texto.lower()

        # Separa las letras de sus diacríticos
        texto = unicodedata.normalize('NFD', texto)

        # Elimina los caracteres de tipo marca diacrítica (Mn), es decir, las tildes y diéresis
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

        # Tokenizar (dividir en palabras)
        palabras = texto.split()

        # Filtrar palabras muy cortas
        palabras = [p for p in palabras if len(p) > 3]

        return palabras

    def entrenar(self, datos):
        """
        Entrena el clasificador con ejemplos de texto etiquetados.

        Args:
            datos (list): Lista de tuplas cuyo primer valor es el contenido
                          del ticket y el segundo valor, la categoría
                          correspondiente.
        """
        print(f"Entrenando clasificador con {len(datos)} ejemplos...")
        for texto, categoria in datos:
            palabras = self.preprocesar_texto(texto)

            # Actualizar contadores
            self.categorias.add(categoria)
            self.tickets_por_categoria[categoria] += 1

            # Contar frecuencia de cada palabra en esta categoría
            for palabra in palabras:
                self.palabras_por_categoria[categoria][palabra] += 1
                self.vocabulario.add(palabra)

        print(f"Entrenamiento completado:")
        print(f"   * Categorías: {sorted(self.categorias)}")
        print(f"   * Vocabulario: {len(self.vocabulario)} palabras únicas")
        for cat in sorted(self.categorias):
            print(f"   * '{cat}': {self.tickets_por_categoria[cat]} tickets")

    def calcular_probabilidad_palabra(self, palabra, categoria):
        """
        Calcula P(palabra|categoria) usando suavizado de Laplace.
        El suavizado evita probabilidades de 0 para palabras no vistas.

        Args:
            palabra (str): Palabra a evaluar
            categoria (str): Categoría a evaluar

        Returns:
            float: Probabilidad de la palabra dada la categoría
        """
        # Frecuencia de la palabra en esta categoría
        frecuencia_palabra = self.palabras_por_categoria[categoria][palabra]

        # Total de palabras en esta categoría
        total_palabras_categoria = sum(self.palabras_por_categoria[categoria].values())

        # Suavizado de Laplace: sumamos 1 al numerador y |vocabulario| al denominador
        # Esto evita probabilidades de 0 para palabras nuevas
        probabilidad = (frecuencia_palabra + 1) / (total_palabras_categoria + len(self.vocabulario))

        return probabilidad

    def clasificar(self, texto):
        """
        Clasifica un texto usando el teorema de Bayes.
        P(categoria|texto) ∝ P(categoria) * ∏P(palabra|categoria)

        Args:
            texto (str): Texto a clasificar

        Returns:
            dict: Probabilidades por categoría
        """
        palabras = self.preprocesar_texto(texto)

        # Convertimos las probabilidades a logaritmos para evitar underflow
        # (multiplicar muchas probabilidades pequeñas da números muy pequeños)
        log_probabilidades = {}

        for categoria in sorted(self.categorias):
            # P(categoria) = tickets_categoria / total_tickets
            total_tickets = sum(self.tickets_por_categoria.values())
            prob_categoria = self.tickets_por_categoria[categoria] / total_tickets

            # Empezamos con log(P(categoria))
            log_prob = math.log(prob_categoria)

            # Multiplicamos por P(palabra|categoria) para cada palabra
            # En log-space: log(a*b) = log(a) + log(b)
            for palabra in palabras:
                prob_palabra = self.calcular_probabilidad_palabra(palabra, categoria)
                log_prob += math.log(prob_palabra)

            log_probabilidades[categoria] = log_prob

        # Convertir las probabilidades logarítmicas de vuelta a probabilidades normales
        # Usamos el truco: exp(log_prob - max_log_prob) para estabilidad numérica
        max_log_prob = max(log_probabilidades.values())
        probabilidades = {}

        for categoria, log_prob in log_probabilidades.items():
            probabilidades[categoria] = math.exp(log_prob - max_log_prob)

        # Normalizar para que sumen 1
        # Sumamos todos los números en `probabilidades`
        # Dividimos cada probabilidad por el total de probabilidades y así
        # conseguimos que los valores de probabilidad de cada categoría se
        # transforme en una proporción que sumadas dan 1.
        total = sum(probabilidades.values())
        for categoria in probabilidades:
            probabilidades[categoria] /= total

        return probabilidades

    def palabras_mas_representativas(self, n=10):
        """
        Encuentra las palabras que mejor distinguen entre categorías.
        Útil para entender lo que aprendió el modelo.
        """
        print(f"\nTOP {n} PALABRAS MÁS REPRESENTATIVAS POR CATEGORÍA:")
        print("=" * 60)

        for categoria in sorted(self.categorias):
            # Calculamos la "representatividad" de cada palabra
            # usando la frecuencia relativa en esta categoría vs otras
            scores = {}

            for palabra in sorted(self.vocabulario):
                freq_categoria = self.palabras_por_categoria[categoria][palabra]
                total_categoria = sum(self.palabras_por_categoria[categoria].values())

                # Frecuencia en otras categorías
                freq_otras = 0
                total_otras = 0
                for otra_cat in self.categorias:
                    if otra_cat != categoria:
                        freq_otras += self.palabras_por_categoria[otra_cat][palabra]
                        total_otras += sum(self.palabras_por_categoria[otra_cat].values())

                if total_otras > 0:
                    # Relación de frecuencias relativas
                    rel_freq_cat = (freq_categoria + 1) / (total_categoria + len(self.vocabulario))
                    rel_freq_otras = (freq_otras + 1) / (total_otras + len(self.vocabulario))
                    scores[palabra] = rel_freq_cat / rel_freq_otras

            # Mostrar palabras mas representativas
            top_palabras = sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:n]

            print(f"\n  {categoria.upper()}:")
            for palabra, score in top_palabras:
                print(f"   * {palabra:<15} (score: {score:.2f})")


# Ejemplo práctico: Clasificador de tickets de soporte
if __name__ == "__main__":
    # Datos de entrenamiento simulando tickets de soporte técnico
    # Cada elemento de la lista contiene una tupla compuesta por
    # la descripción del ticket y la categoría a la que pertenece.
    datos_de_entrenamiento = [
        ("La aplicación se cierra inesperadamente al hacer click en enviar", "BUG"),
        ("Error 500 al intentar subir archivo grande", "BUG"),
        ("El botón de guardar no funciona en Firefox", "BUG"),
        ("Pantalla en blanco después de iniciar sesión", "BUG"),
        ("Los datos no se actualizan correctamente en la tabla", "BUG"),
        ("Mensaje de error extraño al procesar el pago", "BUG"),
        ("Sería genial poder exportar reportes a Excel", "FEATURE"),
        ("Necesitamos filtros avanzados en el listado de productos", "FEATURE"),
        ("Propongo agregar notificaciones push para mensajes", "FEATURE"),
        ("Falta la opción de cambiar el idioma de la interfaz", "FEATURE"),
        ("Queremos integración con Google Calendar", "FEATURE"),
        ("Deberíamos tener dashboard personalizable para cada usuario", "FEATURE"),
        ("Cómo puedo cambiar mi contraseña", "SUPPORT"),
        ("No entiendo cómo funciona el sistema de permisos", "SUPPORT"),
        ("Necesito ayuda para configurar mi perfil", "SUPPORT"),
        ("Dónde encuentro las estadísticas de ventas", "SUPPORT"),
        ("Instrucciones para conectar con la API", "SUPPORT"),
        ("Tutorial para usar las funciones avanzadas", "SUPPORT")
    ]

    # Crear y entrenar el clasificador
    clasificador = ClasificadorTextoBasico()
    clasificador.entrenar(datos_de_entrenamiento)

    # Probar con tickets nuevos
    print("\n\nPROBANDO CLASIFICADOR CON TICKETS NUEVOS:")
    print("=" * 60)

    tickets_prueba = [
        "La pagina queda en blanco cuando cargo muchos productos",
        "Me gustaría poder ordenar la lista por fecha de creación",
        "No sé cómo resetear mi cuenta de usuario"
    ]

    for i, ticket in enumerate(tickets_prueba, 1):
        print(f"\n#{i}: '{ticket}'")

        resultados = clasificador.clasificar(ticket)

        # Mostrar probabilidades ordenadas
        for categoria, prob in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
            print(f"   {categoria}: {prob:.1%}")

        # Mostrar predicción final
        mejor_categoria = max(resultados.items(), key=lambda x: x[1])
        print(f"   -> CLASIFICACIÓN: {mejor_categoria[0]} ({mejor_categoria[1]:.1%} confianza)")

    # Mostrar palabras más representativas
    clasificador.palabras_mas_representativas(15)
