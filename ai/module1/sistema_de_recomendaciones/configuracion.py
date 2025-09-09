import yaml
from typing import Dict


class Configuracion:
    """
    Carga y valida configuraciones desde archivos YAML.
    Proporciona valores por defecto robustos en caso de archivos faltantes.
    Funcionalidades:
    - Carga configuración desde YAML
    - Validación de tipos y valores
    - Valores por defecto seguros
    - Actualización dinámica de reglas
    """

    def __init__(self, archivo_config: str):
        """
        Inicializa la configuración del sistema.

        Args:
            archivo_config: Ruta al archivo YAML de configuración
        """
        self.config = {}

        print(f"Cargando la configuración desde {archivo_config}")
        try:
            with open(archivo_config, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
                print(f"Configuración cargada desde {archivo_config}")
                self.validar_configuracion()
        except yaml.YAMLError as e:
            print(f"Error al cargar el archivo YAML: {e}")
            raise
        except FileNotFoundError:
            print(f"Archivo {archivo_config} no encontrado")
            raise
        except ValueError as e:
            print(e)
            raise

    def validar_configuracion(self):
        """
        Verifica que los valores estén en rangos válidos y sean consistentes.
        """
        errores = []

        # Pesos de los algoritmos
        algoritmos = self.get_pesos_algoritmos()
        suma_pesos = algoritmos["filtrado_colaborativo"] + \
            algoritmos["filtrado_contenido"]
        if abs(suma_pesos - 1.0) > 0.01:  # Tolerancia para errores de punto flotante
            errores.append(
                f"Los pesos de algoritmos deben sumar 1.0, actual: {suma_pesos}")

        # Validar pesos de similitud
        similitud = self.get_pesos_similitud()
        suma_pesos = similitud["peso_productos"] + \
            similitud["peso_demografica"] + similitud["peso_intereses"]
        if abs(suma_pesos - 1.0) > 0.01:
            errores.append(
                f"Los pesos de similitud deben sumar 1.0, actual: {suma_pesos}")

        if errores:
            print("Errores de validación encontrados:")
            for error in errores:
                print(f"   * {error}")
            raise ValueError("Configuración inválida")

        print("Configuración validada exitosamente")

    def get_pesos_algoritmos(self) -> Dict[str, float]:
        """Obtiene pesos para combinar algoritmos"""
        valor_por_defecto = {
            "filtrado_colaborativo": 0.6,
            "filtrado_contenido": 0.4
        }
        return self.config.get("pesos_algoritmos", valor_por_defecto)

    def get_pesos_puntuacion_contenido(self) -> Dict[str, float]:
        """"Obtiene los pesos para la puntuacion por contenido"""
        valor_por_defecto = {
            "peso_interes_categoria": 2.0,
            "peso_interes_etiquetas": 1.5,
            "peso_edad_apropiada": 1.5,
            "peso_valoracion": 1.0,
            "peso_popularidad": 1.0,
            "peso_precio_apropiado": 1.0,
            "penalizacion_precio": -0.2,
            "precio_minimo_para_nivel_gasto_alto": 50000,
            "peso_maximo_para_nivel_de_gasto_bajo": 15000
        }
        return self.config.get("puntuacion_contenido", valor_por_defecto)

    def get_pesos_similitud(self) -> Dict[str, float]:
        """Obtiene pesos para cálculo de similitud"""
        valor_por_defecto = {
            "boost_mismo_genero": 0.2,
            "boost_misma_ubicacion": 0.2,
            "peso_productos": 0.4,
            "peso_demografica": 0.3,
            "peso_intereses": 0.3,
            "tolerancia_edad": 10
        }
        return self.config.get("similitud_usuarios", valor_por_defecto)

    def get_peso_puntuacion_interes_categoria(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con el interes por la categoria"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["peso_interes_categoria"]

    def get_peso_puntuacion_interes_etiquetas(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con el interes por las etiquetas"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["peso_interes_etiquetas"]

    def get_peso_puntuacion_edad_apropiada(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con la edad objetivo"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["peso_edad_apropiada"]

    def get_peso_puntuacion_valoracion(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con la valoracion"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["peso_valoracion"]

    def get_peso_puntuacion_popularidad(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con la popularidad"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["peso_popularidad"]

    def get_peso_puntuacion_precio_apropiado(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con el precio"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["peso_precio_apropiado"]

    def get_peso_puntuacion_penalizacion_precio(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con la penalizacion por precio"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["penalizacion_precio"]

    def get_peso_puntuacion_precio_minimo_para_nivel_gasto_alto(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con el precio minimo para un nivel de gasto alto"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["precio_minimo_para_nivel_gasto_alto"]

    def get_peso_puntuacion_peso_maximo_para_nivel_de_gasto_bajo(self):
        """Devuelve el peso de la puntuacion por contenido relacionada con el precio maximo para un nivel de gasto bajo"""
        puntuacion_contenido = self.get_pesos_puntuacion_contenido()
        return puntuacion_contenido["peso_maximo_para_nivel_de_gasto_bajo"]

    def get_peso_algoritmo_filtrado_colaborativo(self):
        """Devuelve el peso del algoritmo de filtrado colaborativo"""
        algoritmos = self.get_pesos_algoritmos()
        return algoritmos["filtrado_colaborativo"]

    def get_peso_algoritmo_filtrado_contenido(self):
        """Devuelve el peso del algoritmo de filtrado por contenido"""
        algoritmos = self.get_pesos_algoritmos()
        return algoritmos["filtrado_contenido"]

    def get_peso_similitud_por_productos(self):
        """Devuelve el peso para la similitud por productos"""
        similitud = self.get_pesos_similitud()
        return similitud["peso_productos"]

    def get_peso_similitud_demografica(self):
        """Devuelve el peso para la similitud demografica"""
        similitud = self.get_pesos_similitud()
        return similitud["peso_demografica"]

    def get_peso_similitud_por_intereses(self):
        """Devuelve el peso para la similitud por intereses"""
        similitud = self.get_pesos_similitud()
        return similitud["peso_intereses"]

    def get_tolerancia_por_edad_similar(self):
        """Devuelve el valor de tolerancia por edad similar"""
        similitud = self.get_pesos_similitud()
        return similitud["tolerancia_edad"]

    def get_boost_por_mismo_genero(self):
        """Devuelve el valor para el boost por mismo genero en similitud demográfica"""
        similitud = self.get_pesos_similitud()
        return similitud["boost_mismo_genero"]

    def get_boost_por_misma_ubicacion(self):
        """Devuelve el valor para el boost por misma ubicación en similitud demográfica"""
        similitud = self.get_pesos_similitud()
        return similitud["boost_misma_ubicacion"]
