class DiagnosticadorRendimiento:
    """
    Sistema experto para diagnosticar problemas de rendimiento
    en aplicaciones web usando reglas lógicas.
    """

    def __init__(self):
        # Base de conocimiento: conjunto de reglas de diagnóstico
        self.reglas = [
            self._regla_base_datos,
            self._regla_red,
            self._regla_concurrencia
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
                    'Optimizar tamaño de respuestas (compresión)',
                    'Revisar configuración de firewall/proxy'
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
                    'Usar load balancing con múltiples instancias',
                    'Optimizar connection pooling',
                    'Implementar queue para procesos no críticos'
                ]
            }
        return None


# Ejemplo de uso del sistema experto
if __name__ == "__main__":
    # Creamos una instancia de nuestro diagnosticador
    diagnosticador = DiagnosticadorRendimiento()

    # Simulamos métricas de un servidor con problemas
    metricas_servidor = {
        'tiempo_respuesta': 4.2,    # 4.2 segundos promedio
        'uso_memoria': 92,          # 92% de memoria utilizada
        'queries_lentas': 15,       # 15 queries tardan más de 1s
        'conexiones_activas': 800,  # 800 conexiones simultáneas
        'uso_cpu': 45              # 45% de CPU utilizada
    }

    # Realizamos el diagnóstico
    print("🔍 DIAGNÓSTICO DEL SISTEMA")
    print("=" * 50)

    resultados = diagnosticador.diagnosticar(metricas_servidor)

    if not resultados:
        print("✅ No se detectaron problemas significativos")
    else:
        for i, diagnostico in enumerate(resultados, 1):
            print(f"\n#{i} - {diagnostico['problema']}")
            print(f"Certeza: {diagnostico['certeza']:.1%}")
            print("Recomendaciones:")
            for rec in diagnostico['recomendaciones']:
                print(f"  • {rec}")
