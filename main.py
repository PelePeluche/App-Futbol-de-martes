from fastapi import FastAPI
from fastapi import HTTPException
from typing import Optional
from datetime import date
from models import (
    cargar_partido,
    cargar_equipo,
    crear_partido,
    crear_jugador,
    get_id_proximo_partido,
    get_partidos,
    get_partido_by_id,
    get_lista_de_jugadores_by_partido_by_equipo,
    get_goles_by_partido_by_equipo,
    get_jugadores,
    get_jugador_by_id,
    get_lista_de_jugadores_anotados_by_partido_id,
    get_jugador_by_nombre,
    agregar_jugador_a_proximo_partido,
    quitar_jugador_de_proximo_partido,
    get_lista_jugadores_with_min_partidos,
)
from services.build_teams import armar_equipos_voraz


app = FastAPI()


# Endpoint que detalla los partidos jugados


@app.get("/partidos")
async def listar_partidos():
    try:
        partidos = get_partidos()
        return [
            {
                "Partido": p.id_partido,
                "Equipo 1": [
                    jugador.nombre
                    for jugador in get_lista_de_jugadores_by_partido_by_equipo(p, 0)
                ],
                "Goles Equipo 1": get_goles_by_partido_by_equipo(p, 0),
                "Equipo 2": [
                    jugador.nombre
                    for jugador in get_lista_de_jugadores_by_partido_by_equipo(p, 1)
                ],
                "Goles Equipo 2": get_goles_by_partido_by_equipo(p, 1),
            }
            for p in partidos
            if p.jugado
        ]
    except Exception as error:
        raise error


# Endpoint que detalla un partido en particular
# Recibe como parámetro el id del partido


@app.get("/partidos/{id_partido}")
async def detalle_partido(id_partido: int):
    try:
        partido = get_partido_by_id(id_partido)
        if partido.jugado:
            return {
                "Partido": partido.id_partido,
                "Equipo 1": [
                    jugador.nombre
                    for jugador in get_lista_de_jugadores_by_partido_by_equipo(partido, 0)
                ],
                "Goles Equipo 1": get_goles_by_partido_by_equipo(partido, 0),
                "Equipo 2": [
                    jugador.nombre
                    for jugador in get_lista_de_jugadores_by_partido_by_equipo(partido, 1)
                ],
                "Goles Equipo 2": get_goles_by_partido_by_equipo(partido, 1),
            }
        else:
             return {
                "Partido": partido.id_partido,
                "Jugadores anotados": [
                    jugador.nombre
                    for jugador in get_lista_de_jugadores_anotados_by_partido_id(
                        get_id_proximo_partido()
                    )
                ],
            }
            
    except Exception as error:
        raise error


# Endpoint que carga datos de un partido
# Recibe como parámetro el id del partido, los jugadores de cada equipo, los goles, pecheras (Optional) y fecha (Optional)


@app.put("/partidos/{id_partido}")
async def carga_partido_jugado(
    id_partido: int,
    jugadores_equipo_1: list,
    goles_equipo_1: int,
    jugadores_equipo_2: list,
    goles_equipo_2: int,
    nombre_cancha: Optional[str] = None,
    fecha: Optional[date] = None,
    pecheras_equipo_1: Optional[str] = None,
    pecheras_equipo_2: Optional[str] = None,
):
    try:
        e1 = cargar_equipo(
            id_partido, jugadores_equipo_1, goles_equipo_1, pecheras_equipo_1
        )
        e2 = cargar_equipo(
            id_partido, jugadores_equipo_2, goles_equipo_2, pecheras_equipo_2
        )
        partido = cargar_partido(
            id_partido, e1.id_equipo, e2.id_equipo, nombre_cancha, fecha
        )
        return partido
    except Exception as error:
        raise error


# Endpoint que detalla el próximo partido

# No voy a usar este endpoint pero lo dejo un tiempo por si las dudas
"""
@app.get("/proximo-partido")
async def detalle_proximo_partido():
    try:
        partido = get_partido_by_id(get_id_proximo_partido())
        if not partido.jugado:
            return {
                "Partido": partido.id_partido,
                "Jugadores anotados": [
                    jugador.nombre
                    for jugador in get_lista_de_jugadores_anotados_by_partido_id(
                        get_id_proximo_partido()
                    )
                ],
            }
        else:
            print("No hay un próximo partido programado")
    except Exception as error:
        raise error
"""

# Endpoint para crear el próximo partido


@app.post("/proximo-partido")
async def crear_proximo_partido():
    try:
        partido = crear_partido()
        return partido
    except Exception as error:
        raise error


# Endpoint para agregar un jugador al próximo partido
# Recibe como parámetro el nombre del jugador a agregar


@app.put("/proximo-partido/agregar-jugador")
async def agregar_jugador(nombre_jugador: str):
    try:
        return agregar_jugador_a_proximo_partido(nombre_jugador)
    except Exception as error:
        raise error


# Endpoint para quitar un jugador del próximo partido
# Recibe como parámetro el nombre del jugador a quitar


@app.put("/proximo-partido/eliminar-jugador")
async def quitar_jugador(nombre_jugador: str):
    try:
        return quitar_jugador_de_proximo_partido(nombre_jugador)
    except Exception as error:
        raise error


# Endpoint para armar los equipos del próximo partido
# Recibe como parámetro la cantidad de jugadores de los equipos.
# La idea es que más adelante reciba como parámetro el tipo de algoritmo a utilizar


@app.get("/proximo-partido/arma-equipos")
async def armar_equipos_voraz_proximo_partido(cantidad_jugadores: int):
    try:
        return armar_equipos_voraz(get_id_proximo_partido(), int(cantidad_jugadores))
    except Exception as error:
        raise error


# Endopoint que detalla la lista de jugadores


@app.get("/jugadores")
async def listar_jugadores():
    try:
        jugadores = get_jugadores()
        return [
            {
                "Jugador": j.nombre,
                "Partidos jugados": j.jugados,
                "Puntos": j.puntos,
                "Promedio": j.promedio,
            }
            for j in jugadores
        ]
    except Exception as error:
        raise error


# Endpoint para crear nuevos jugadores
# Recibe como parámetro el nombre del jugador


@app.post("/jugadores")
async def crear_nuevo_jugador(nombre_jugador: str):
    try:
        jugador = crear_jugador(nombre_jugador)
        return jugador
    except Exception as error:
        raise error


# Endpoint que detalla un jugador en particular
# Recibe como parámetro el nombre del jugador


@app.get("/jugadores/{nombre_jugador}")
async def detalle_jugador(nombre_jugador: str):
    try:
        jugador = get_jugador_by_nombre(nombre_jugador)
        return {
            "Jugador": jugador.nombre,
            "Partidos jugados": jugador.jugados,
            "Puntos": jugador.puntos,
            "Promedio": jugador.promedio,
            "Resultados": {
                "Ganados": jugador.get_resultados()["ganados"],
                "Empatados": jugador.get_resultados()["empatados"],
                "Perdidos": jugador.get_resultados()["perdidos"],
            },
        }
    except Exception as error:
        raise error


# Función que obtiene la tabla de promedios ordenados de mayor a menor mostrando promedio de puntos, promedio de goles, partidos ganados, empatados, perdidos y cantidad de partidos
# Recibe como parámetro la cantidad de jugadores a mostrar en la lista y el mínimo de partidos jugados


@app.get("/tabla-promiedos")
async def tabla_promiedos(
    minimo_de_partidos: Optional[int] = 0, cantidad_de_jugadores: Optional[int] = None
):
    try:
        tabla_jugadores = get_lista_jugadores_with_min_partidos(
            minimo_de_partidos, cantidad_de_jugadores
        )
        return [
            {
                "Jugador": j.nombre,
                "Promedio": j.promedio,
                "Partidos jugados": j.jugados,
                "Puntos": j.puntos,
            }
            for j in tabla_jugadores
        ]
    except Exception as error:
        raise error
