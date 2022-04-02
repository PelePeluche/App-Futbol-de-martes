from fastapi import FastAPI
import pony.orm as pony
from models import (
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
)
from services.build_teams import armar_equipos_voraz


app = FastAPI()


@app.get("/partidos-jugados")
async def listar_partidos():
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
    ]


@app.get("/partidos-jugados/{id_partido}")
async def detalle_partido(id_partido: int):
    partido = get_partido_by_id(id_partido)
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


@app.get("/proximo-partido")
async def detalle_proximo_partido():
    partido = get_partido_by_id(get_id_proximo_partido())
    return {
        "Partido": partido.id_partido,
        "Jugadores anotados": [
            jugador.nombre
            for jugador in get_lista_de_jugadores_anotados_by_partido_id(
                get_id_proximo_partido()
            )
        ],
    }


@app.post("/proximo-partido")
async def crear_proximo_partido():
    partido = crear_partido()
    return partido


@app.put("/proximo-partido")
async def agregar_jugador(nombre_jugador):
    with pony.db_session():
        partido = get_partido_by_id(get_id_proximo_partido())
        jugador = get_jugador_by_nombre(nombre_jugador)
        partido.add_jugador(jugador)
        return partido


@app.get("/proximo-partido/equipos")
async def armar_equipos_voraz_proximo_partido(cantidad_jugadores):
    return armar_equipos_voraz(get_id_proximo_partido(), int(cantidad_jugadores))


@app.get("/jugadores")
async def listar_jugadores():
    jugadores = get_jugadores()
    return [
        {
            "Jugador": j.nombre,
            "Partidos jugados": j.get_jugados(),
            "Puntos": j.get_puntos(),
            "Promedio": j.get_promedio(),
        }
        for j in jugadores
    ]


@app.post("/jugadores")
async def crear_nuevo_jugador(nombre_jugador):
    jugador = crear_jugador(nombre_jugador)
    return jugador


@app.get("/jugadores/{nombre_jugador}")
async def detalle_jugador(nombre_jugador):
    jugador = get_jugador_by_nombre(nombre_jugador)
    return {
        "Jugador": jugador.nombre,
        "Partidos jugados": jugador.get_jugados(),
        "Puntos": jugador.get_puntos(),
        "Promedio": jugador.get_promedio(),
        "Resultados": {
            "Ganados": jugador.get_resultados()["ganados"],
            "Empatados": jugador.get_resultados()["empatados"],
            "Perdidos": jugador.get_resultados()["perdidos"],
        },
    }
