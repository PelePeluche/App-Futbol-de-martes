from models import (
    get_jugadores,
    get_lista_equipos_juntos,
    get_lista_de_jugadores_anotados_by_partido_id,
)
import pandas as pd

# Función para crear la matriz con puntos entre jugadores


def base_matriz():
    jugadores_nombres = [j.nombre for j in get_jugadores()]
    return pd.DataFrame(
        columns=jugadores_nombres,
        index=jugadores_nombres,
    )


# Función que obtiene la lista de resultados obtenidos entre dos jugadores estando en el mismo equipo


def get_lista_resultados_juntos(nombre_jugador_1, nombre_jugador_2):
    equipos_juntos = get_lista_equipos_juntos(nombre_jugador_1, nombre_jugador_2)
    lista_resultados = [equipo.resultado for equipo in equipos_juntos]
    return lista_resultados


# Función que obtiene los puntos obtenidos entre dos jugadores estando en el mismo equipo


def puntos_jugando_juntos(nombre_jugador_1, nombre_jugador_2):
    return sum(get_lista_resultados_juntos(nombre_jugador_1, nombre_jugador_2))


# Función que obtiene el promedio de puntos obtenidos entre dos jugadores estando en el mismo equipo


def promedio_jugando_juntos(nombre_jugador_1, nombre_jugador_2):
    lista_resultados_juntos = get_lista_resultados_juntos(
        nombre_jugador_1, nombre_jugador_2
    )
    try:
        return sum(lista_resultados_juntos) / len(lista_resultados_juntos)
    except:
        raise ("No se pudo obtener el promedio entre esos jugadores")


# Función para completar la matriz con puntos entre jugadores


def completar_matriz(df):
    jugadores = df.columns.values
    count_1 = 0
    while count_1 < len(jugadores):
        nombre_jugador_1 = jugadores[count_1]
        count_2 = 0
        while count_2 < len(jugadores):
            nombre_jugador_2 = jugadores[count_2]
            if (
                len(get_lista_resultados_juntos(nombre_jugador_1, nombre_jugador_2))
                == 0
            ):
                df.iloc[count_1, count_2] = 0
            else:
                df.iloc[count_1, count_2] = round(
                    promedio_jugando_juntos(nombre_jugador_1, nombre_jugador_2), 1
                )
            count_2 += 1
        count_1 += 1


# Función para obtener el mejor jugador (de los anotados para un partido) para un equipo dado


def proximo_jugador(candidatos, jugadores_equipo, df):
    valoracion = 0
    anotar_jugador = 0
    for candidato in candidatos:
        conteo = 0
        for jugador in jugadores_equipo:
            conteo += df.loc[candidato][jugador]
        if conteo > valoracion:
            valoracion = conteo
            anotar_jugador = candidato
    if anotar_jugador == 0:
        for candidato in candidatos:
            if df.loc[candidato][candidato] > valoracion:
                valoracion = df.loc[candidato][candidato]
                anotar_jugador = candidato
    return anotar_jugador


# Función para armar los equipos para un partido de manera voraz


def armar_equipos_voraz(partido_id, cantidad_jugadores):
    df = base_matriz()
    completar_matriz(df)
    jugadores_anotados = [
        jugador.nombre
        for jugador in get_lista_de_jugadores_anotados_by_partido_id(partido_id)
    ]
    equipo_1 = []
    equipo_2 = []
    while len(equipo_2) < cantidad_jugadores:
        if len(equipo_1) <= len(equipo_2):
            jugador_a_agregar = proximo_jugador(jugadores_anotados, equipo_1, df)
            equipo_1.append(jugador_a_agregar)
        else:
            jugador_a_agregar = proximo_jugador(jugadores_anotados, equipo_2, df)
            equipo_2.append(jugador_a_agregar)
        jugadores_anotados.remove(jugador_a_agregar)
    print(equipo_1)
    print(equipo_2)
