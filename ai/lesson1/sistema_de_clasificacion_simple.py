import re
from collections import defaultdict, Counter
import math

class ClasificadorTextoBasico:
    """
    Clasificador de texto usando probabilidades bayesianas básicas.
    Útil para clasificar emails, reseñas, tickets de soporte, etc.
    """

    def __init__(self):
        # Almacena las frecuencias de palabras por categoría
        self.palabras_por_categoria = defaultdict(Counter)
        # Almacena cuántos documentos hay por categoría
        self.documentos_por_categoria = defaultdict(int)
        # Lista de todas las categorías conocidas
        self.categorias = set()
        # Vocabulario total (todas las palabras únicas)
        self.vocabulario = set()

    def preprocesar_texto(self, texto):
        """
        Limpia y tokeniza el texto de entrada.

        Args:
            texto (str): Texto a procesar

        Returns:
            list: Lista de palabras limpias en minúsculas
        """
        # Convertir a minúsculas
        texto = texto.lower()

        # Remover puntuación y caracteres especiales
        texto = re.sub(r'[^a-záéíóúñü\s]', ' ', texto)

        # Tokenizar (dividir en palabras)
        palabras = texto.split()

        # Filtrar palabras muy cortas (menos de 3 caracteres)
        palabras = [p for p in palabras if len(p) >= 3]

        return palabras

    def entrenar(self, textos, categorias):
        """
        Entrena el clasificador con ejemplos de texto etiquetados.

        Args:
            textos (list): Lista de strings con el contenido
            categorias (list): Lista de strings con las categorías correspondientes
        """
        print(f"🎯 Entrenando clasificador con {len(textos)} ejemplos...")

        for texto, categoria in zip(textos, categorias):
            # Procesar el texto
            palabras = self.preprocesar_texto(texto)

            # Actualizar contadores
            self.categorias.add(categoria)
            self.documentos_por_categoria[categoria] += 1

            # Contar frecuencia de cada palabra en esta categoría
            for palabra in palabras:
                self.palabras_por_categoria[categoria][palabra] += 1
                self.vocabulario.add(palabra)

        print(f"✅ Entrenamiento completado:")
        print(f"   • Categorías: {list(self.categorias)}")
        print(f"   • Vocabulario: {len(self.vocabulario)} palabras únicas")
        for cat in self.categorias:
            print(f"   • '{cat}': {self.documentos_por_categoria[cat]} documentos")

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

        # Calculamos log-probabilidades para evitar underflow
        # (multiplicar muchas probabilidades pequeñas da números muy pequeños)
        log_probabilidades = {}

        for categoria in self.categorias:
            # P(categoria) = documentos_categoria / total_documentos
            total_documentos = sum(self.documentos_por_categoria.values())
            prob_categoria = self.documentos_por_categoria[categoria] / total_documentos

            # Empezamos con log(P(categoria))
            log_prob = math.log(prob_categoria)

            # Multiplicamos por P(palabra|categoria) para cada palabra
            # En log-space: log(a*b) = log(a) + log(b)
            for palabra in palabras:
                prob_palabra = self.calcular_probabilidad_palabra(palabra, categoria)
                log_prob += math.log(prob_palabra)

            log_probabilidades[categoria] = log_prob

        # Convertir de vuelta a probabilidades normales
        # Usamos el truco: exp(log_prob - max_log_prob) para estabilidad numérica
        max_log_prob = max(log_probabilidades.values())
        probabilidades = {}

        for categoria, log_prob in log_probabilidades.items():
            probabilidades[categoria] = math.exp(log_prob - max_log_prob)

        # Normalizar para que sumen 1
        total = sum(probabilidades.values())
        for categoria in probabilidades:
            probabilidades[categoria] /= total

        return probabilidades

    def palabras_mas_informativas(self, n=10):
        """
        Encuentra las palabras que mejor distinguen entre categorías.
        Útil para entender qué aprendió el modelo.
        """
        print(f"\n📊 TOP {n} PALABRAS MÁS INFORMATIVAS POR CATEGORÍA:")
        print("=" * 60)

        for categoria in self.categorias:
            # Calculamos la "informatividad" de cada palabra
            # usando la frecuencia relativa en esta categoría vs otras
            scores = {}

            for palabra in self.vocabulario:
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
                    # Ratio de frecuencias relativas
                    rel_freq_cat = (freq_categoria + 1) / (total_categoria + len(self.vocabulario))
                    rel_freq_otras = (freq_otras + 1) / (total_otras + len(self.vocabulario))
                    scores[palabra] = rel_freq_cat / rel_freq_otras

            # Mostrar top palabras
            top_palabras = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]

            print(f"\n🏷️  {categoria.upper()}:")
            for palabra, score in top_palabras:
                print(f"   • {palabra:<15} (score: {score:.2f})")


# Ejemplo práctico: Clasificador de tickets de soporte
if __name__ == "__main__":
    # Datos de entrenamiento simulando tickets de soporte técnico
    tickets_entrenamiento = [
        # Tickets de BUG
        "La aplicación se cierra inesperadamente al hacer click en enviar",
        "Error 500 al intentar subir archivo grande",
        "El botón de guardar no funciona en Firefox",
        "Pantalla en blanco después de iniciar sesión",
        "Los datos no se actualizan correctamente en la tabla",
        "Mensaje de error extraño al procesar el pago",

        # Tickets de FEATURE (nuevas funcionalidades)
        "Sería genial poder exportar reportes a Excel",
        "Necesitamos filtros avanzados en el listado de productos",
        "Propongo agregar notificaciones push para mensajes",
        "Falta la opción de cambiar el idioma de la interfaz",
        "Queremos integración con Google Calendar",
        "Deberíamos tener dashboard personalizable para cada usuario",

        # Tickets de SUPPORT (ayuda/consultas)
        "Cómo puedo cambiar mi contraseña",
        "No entiendo cómo funciona el sistema de permisos",
        "Necesito ayuda para configurar mi perfil",
        "Dónde encuentro las estadísticas de ventas",
        "Instrucciones para conectar con la API",
        "Tutorial para usar las funciones avanzadas"
    ]

    categorias_entrenamiento = [
        # Categorías correspondientes a cada ticket
        "BUG", "BUG", "BUG", "BUG", "BUG", "BUG",
        "FEATURE", "FEATURE", "FEATURE", "FEATURE", "FEATURE", "FEATURE",
        "SUPPORT", "SUPPORT", "SUPPORT", "SUPPORT", "SUPPORT", "SUPPORT"
    ]

    # Crear y entrenar el clasificador
    clasificador = ClasificadorTextoBasico()
    clasificador.entrenar(tickets_entrenamiento, categorias_entrenamiento)

    # Mostrar palabras más informativas
    clasificador.palabras_mas_informativas(5)

    # Probar con tickets nuevos
    print("\n\n🔮 PROBANDO CLASIFICADOR CON TICKETS NUEVOS:")
    print("=" * 60)

    tickets_prueba = [
        "La página se congela cuando intento cargar muchos productos",
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
        print(f"   → CLASIFICACIÓN: {mejor_categoria[0]} ({mejor_categoria[1]:.1%} confianza)")
