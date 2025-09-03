class DiagnosticadorRendimiento:
    """
    Sistema experto para diagnosticar problemas de rendimiento
    en aplicaciones web usando reglas lógicas.
    """

    def __init__(self):
        # Base de conocimiento: conjunto de reglas de diagnóstico
        self.reglas = [
            self._regla_cpu,
            self._regla_memoria,
            self._regla_concurrencia,
            self._regla_base_datos,
            self._regla_red
        ]

    def diagnosticar(self, sintomas):
        """
        Diagnostica problemas basándose en los síntomas reportados.

        Args:
            sintomas (dict): Diccionario con métricas del sistema
                - tiempo_respuesta: tiempo promedio en segundos
                - uso_memoria: porcentaje de memoria utilizada
                - queries_lentas: número de queries que tardan >1s
                - conexiones_activas: número de conexiones simultáneas
                - uso_cpu: porcentaje de CPU utilizada

        Returns:
            list: Lista de diagnósticos posibles con sus certezas
        """
        diagnosticos = []

        # Evaluamos cada regla en nuestra base de conocimiento
        for regla in self.reglas:
            resultado = regla(sintomas)
            if resultado:
                diagnosticos.append(resultado)

        # Ordenamos por nivel de certeza (mayor a menor)
        diagnosticos.sort(key=lambda x: x['certeza'], reverse=True)
        return diagnosticos

    def _regla_cpu(self, sintomas):
        """
        Regla: Uso de CPU alto puede indicar procesamiento intensivo o algoritmos ineficientes.
        """
        if sintomas.get('uso_cpu', 0) > 80:
            certeza = min(0.85, sintomas['uso_cpu'] / 100)

            return {
                'problema': 'Procesamiento intensivo o algoritmos ineficientes',
                'certeza': certeza,
                'recomendaciones': [
                    'Analizar el código para identificar cuellos de botella',
                    'Optimizar algoritmos, por ejemplo, aquellos O(n²) o peores',
                    'Implementar una cache para cálculos repetitivos',
                    'Considerar procesamiento asíncrono para tareas pesadas'
                ]
            }
        return None

    def _regla_memoria(self, sintomas):
        """
        Regla: Si el uso de memoria es alto Y el tiempo de respuesta
        es lento, probablemente hay una fuga (leak) de memoria.
        """
        if (sintomas.get('uso_memoria', 0) > 85 and
            sintomas.get('tiempo_respuesta', 0) > 3.0):

            # Calculamos certeza basada en qué tan extremos son los valores
            certeza = min(0.9, (sintomas['uso_memoria'] / 100) *
                         (sintomas['tiempo_respuesta'] / 5))

            return {
                'problema': 'Fuga de memoria o uso excesivo de memoria',
                'certeza': certeza,
                'recomendaciones': [
                    'Revisar objetos no liberados en memoria',
                    'Implementar un grupo de conexiones para evitar abrir y cerrar nuevas',
                    'Analizar el consumo de memoria (memory_profiler)',
                    'Considerar aumentar la cantidad de RAM del servidor'
                ]
            }
        return None

    def _regla_concurrencia(self, sintomas):
        """
        Regla: Muchas conexiones simultáneas pueden saturar el servidor.
        """
        if sintomas.get('conexiones_activas', 0) > 1000:
            certeza = min(0.8, sintomas['conexiones_activas'] / 2000)

            return {
                'problema': 'Sobrecarga por exceso de conexiones concurrentes',
                'certeza': certeza,
                'recomendaciones': [
                    'Implementar rate limiting',
                    'Usar un balanceador de carga (load balancer) con múltiples instancias',
                    'Utilizar un grupo de conexiones preestablecidas',
                    'Implementar colas para procesos no críticos'
                ]
            }
        return None

    def _regla_base_datos(self, sintomas):
        """
        Regla: Si hay muchas queries lentas, el problema está
        en la base de datos.
        """
        if sintomas.get('queries_lentas', 0) > 10:
            certeza = min(0.95, sintomas['queries_lentas'] / 50)

            return {
                'problema': 'Queries de base de datos ineficientes',
                'certeza': certeza,
                'recomendaciones': [
                    'Revisar índices en tablas frecuentemente consultadas',
                    'Optimizar queries con EXPLAIN ANALYZE',
                    'Implementar cache de queries (Redis)',
                    'Considerar particionado de tablas grandes'
                ]
            }
        return None

    def _regla_red(self, sintomas):
        """
        Regla: Si el tiempo de respuesta es alto pero CPU y memoria
        están bien, puede ser un problema de red.
        """
        if (sintomas.get('tiempo_respuesta', 0) > 2.0 and
            sintomas.get('uso_cpu', 0) < 50 and
            sintomas.get('uso_memoria', 0) < 70):

            certeza = 0.7  # Menos certeza porque es por descarte

            return {
                'problema': 'Latencia de red o problemas de conectividad',
                'certeza': certeza,
                'recomendaciones': [
                    'Verificar latencia entre servidor y clientes',
                    'Implementar CDN para recursos estáticos',
                    'Optimizar tamaño de respuestas (compresión)'
                ]
            }
        return None


# Ejemplo de uso del sistema experto
if __name__ == "__main__":
    # Creamos una instancia de nuestro diagnosticador
    diagnosticador = DiagnosticadorRendimiento()

    # Recibimos del usuario los valores de cada metrica
    print("=" * 50)
    print("Ingrese los valores de rendimiento del sistema")
    cpu = int(input("Porcentaje de CPU utilizada(int): "))
    memoria = int(input("Porcentaje de memoria utilizada(int): "))
    tiempo_de_respuesta = float(input("Cantidad de segundos en promedio para recibir una respuesta(float): "))
    queries_lentas = int(input("Cantidad de queries tardan más de 1 segundo(int): "))
    conexiones_activas = int(input("Cantidad de conexiones simultáneas(int): "))

    # Simulamos métricas de un servidor con problemas
    metricas_servidor = {
        'tiempo_respuesta': tiempo_de_respuesta,
        'uso_memoria': memoria,
        'queries_lentas': queries_lentas,
        'conexiones_activas': conexiones_activas,
        'uso_cpu': cpu
    }

    # Realizamos el diagnóstico
    print("=" * 50)
    print("DIAGNÓSTICO DEL SISTEMA")
    print("=" * 50)

    resultados = diagnosticador.diagnosticar(metricas_servidor)

    if not resultados:
        print("No se detectaron problemas significativos")
    else:
        for i, diagnostico in enumerate(resultados, 1):
            print(f"\n#{i} - {diagnostico['problema']}")
            print(f"Certeza: {diagnostico['certeza']:.1%}")
            print("Recomendaciones:")
            for rec in diagnostico['recomendaciones']:
                print(f"  • {rec}")
