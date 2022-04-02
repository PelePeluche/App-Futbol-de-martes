from fastapi import FastAPI
import pony.orm as pony
from models import (
    db,
    get_partidos,
    get_partido_by_id,
    get_lista_de_jugadores_by_partido_by_equipo,
    get_goles_by_partido_by_equipo,
    get_jugadores,
    get_jugador_by_id,
)

app = FastAPI()


@app.get("/partidos")
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


@app.get("/partidos/{id_partido}")
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


@app.get("/jugadores/{id_jugador}")
async def detalle_jugador(id_jugador):
    jugador = get_jugador_by_id(id_jugador)
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
