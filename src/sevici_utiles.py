from collections import namedtuple
import math

EstacionSevici = namedtuple("EstacionSevici", 
    "nombre, direccion, latitud, longitud, capacidad, puestos_libres, bicicletas_disponibles")

def selecciona_color(estacion:EstacionSevici) -> str:
    """
    Devuelve el color en que debe pintarse cada estación según su disponibilidad.

    Parámetros:
    estacion: EstacionSevici

    Devuelve:
    str: "green", "orange", "red" o "gray"
    """
    if estacion.capacidad == 0 or estacion.bicicletas_disponibles==0:
        return "gray"
    if estacion.bicicletas_disponibles/estacion.capacidad >= (2/3):
        return "green"
    if estacion.bicicletas_disponibles/estacion.capacidad >= (1/3):
            return "orange"
    return "red"

def calcula_estadisticas(estaciones: list[EstacionSevici]) -> tuple[int, int, float, int]:
    """
    Calcula estadísticas de las estaciones.
    Parametros:
    estaciones: lista de EstacionSevici
    Devuelve:
    tupla con (total de bicicletas libres, total de capacidad, porcentaje de ocupación, total de estaciones)
    """
    total_bicis = 0
    total_capacidad = 0
    total_estaciones = 0
    for estacion in estaciones:
        total_bicis += estacion.bicicletas_disponibles
    for estacion in estaciones:
        total_capacidad += estacion.capacidad
    porc_ocupacion = 100-((total_bicis/total_capacidad)*100)
    for estacion in estaciones:
        total_estaciones += 1


    return (total_bicis, total_capacidad, porc_ocupacion, total_estaciones)

def busca_estaciones_direccion(estaciones: list[EstacionSevici], direccion_parcial: str) -> list[EstacionSevici]:
    """
    Busca las estaciones que contengan en su dirección (subcadena, sin distinguir mayúsculas/minúsculas) la dirección parcial dada.    

    Parametros:
    estaciones: lista de EstacionSevici
    direccion_parcial: subcadena a buscar en la dirección de las estaciones

    Devuelve:
    lista de EstacionSevici que cumplen el criterio
    """
    lista_nueva = []
    for estacion in estaciones:
        direccion = estacion.direccion.lower()
        if direccion_parcial.lower() in direccion:
            lista_nueva.append(estacion)
    return lista_nueva

def busca_estaciones_con_disponibilidad(estaciones:list[EstacionSevici], min_disponibilidad: float = 0.5) -> list[EstacionSevici]:
    """
    Devuelve una lista de EstacionSevici con al menos el porcentaje mínimo de bicicletas disponible
    indicado.

    Parametros:
    estaciones: lista de EstacionSevici
    min_disponibilidad: porcentaje mínimo de bicicletas disponibles (0.0 a 1.0)
    
    Devuelve:
    lista de EstacionSevici
    """
    lista_nueva = []
    for estacion in estaciones:
        if estacion.bicicletas_disponibles == 0 or estacion.capacidad==0:
            disponibilidad = 0
        else:
            disponibilidad = estacion.bicicletas_disponibles / estacion.capacidad
            if disponibilidad >= min_disponibilidad:
                lista_nueva.append(estacion)
    return lista_nueva

def calcula_distancia(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calcula la distancia euclídea entre dos puntos (latitud, longitud).

    Parámetros:
    p1: tupla (latitud, longitud) del primer punto
    p2: tupla (latitud, longitud) del segundo punto

    Devuelve:
    float: distancia euclídea entre los dos puntos
    """
    dis_euclidea =math.sqrt ((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    return dis_euclidea

def busca_estacion_mas_cercana(estaciones:list[EstacionSevici], punto:tuple[float, float]) -> EstacionSevici | None:
    """
    Devuelve la estación más cercana al punto dado (latitud, longitud) que tenga al menos una bicicleta disponible.
    
    Parametros:
    estaciones: lista de EstacionSevici
    punto: tupla (latitud, longitud)

    Devuelve:
    EstacionSevici más cercana con al menos una bicicleta disponible, o None si no hay ninguna.
    """ 
    estacion_cercana = None
    dis_menor = None

    for estacion in estaciones:
        if estacion.bicicletas_disponibles>0:
            coord = (estacion.latitud,estacion.longitud)
            if estacion_cercana == None or calcula_distancia(coord,punto)<dis_menor:
                dis_menor = calcula_distancia(coord,punto)
                estacion_cercana = estacion
    return estacion_cercana


    return None

def calcula_ruta(estaciones:list[EstacionSevici], origen:tuple[float, float], destino:tuple[float, float]) -> tuple[EstacionSevici | None, EstacionSevici | None]   :
    """
    Devuelve las estaciones más cercanas al punto de origen y destino dados, que tengan al menos una bicicleta disponible.

    Parametros: 
    estaciones: lista de EstacionSevici
    origen: tupla (latitud, longitud) del punto de origen
    destino: tupla (latitud, longitud) del punto de destino

    Devuelve:
    tupla con (estacion_origen, estacion_destino)
    """
    estacion_cercana_origen = busca_estacion_mas_cercana(estaciones,origen)
    estacion_cercana_destino = busca_estacion_mas_cercana(estaciones,destino)
    return (estacion_cercana_origen,estacion_cercana_destino)
