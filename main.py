from fastapi import FastAPI
from fastapi import HTTPException
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
    agregar_jugador_a_proximo_partido,
    quitar_jugador_de_proximo_partido,
)
from services.build_teams import armar_equipos_voraz


app = FastAPI()


# Endpoint que detalla los partidos jugados


@app.get("/partidos-jugados")
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
        ]
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo acceder a la lista de partidos"
        )


# Endpoint que detalla un partido en particular
# Recibe como parámetro el id del partido


@app.get("/partidos-jugados/{id_partido}")
async def detalle_partido(id_partido: int):
    try:
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
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo acceder al partido solicitado"
        )


# Endpoint que detalla el próximo partido


@app.get("/proximo-partido")
async def detalle_proximo_partido():
    try:
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
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo acceder al partido solicitado"
        )


# Endpoint para crear el próximo partido


@app.post("/proximo-partido")
async def crear_proximo_partido():
    try:
        partido = crear_partido()
        return partido
    except:
        raise HTTPException(status_code=500, detail="No se pudo crear el partido")


# Endpoint para agregar un jugador al próximo partido
# Recibe como parámetro el nombre del jugador a agregar


@app.put("/proximo-partido/agregar-jugador")
async def agregar_jugador(nombre_jugador: str):
    try:
        return agregar_jugador_a_proximo_partido(nombre_jugador)
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo realizar la acción requerida"
        )


# Endpoint para quitar un jugador del próximo partido
# Recibe como parámetro el nombre del jugador a quitar


@app.put("/proximo-partido/eliminar-jugador")
async def quitar_jugador(nombre_jugador: str):
    try:
        return quitar_jugador_de_proximo_partido(nombre_jugador)
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo quitar al jugador del proximo partido"
        )


# Endpoint para armar los equipos del próximo partido
# Recibe como parámetro la cantidad de jugadores de los equipos.
# La idea es que más adelante reciba como parámetro el tipo de algoritmo a utilizar


@app.get("/proximo-partido/arma-equipos")
async def armar_equipos_voraz_proximo_partido(cantidad_jugadores: int):
    try:
        return armar_equipos_voraz(get_id_proximo_partido(), int(cantidad_jugadores))
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo realizar la acción requerida"
        )


# Endopoint que detalla la lista de jugadores


@app.get("/jugadores")
async def listar_jugadores():
    try:
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
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo acceder a la lista de jugadores"
        )


# Endpoint para crear nuevos jugadores
# Recibe como parámetro el nombre del jugador


@app.post("/jugadores")
async def crear_nuevo_jugador(nombre_jugador: str):
    try:
        jugador = crear_jugador(nombre_jugador)
        return jugador
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo realizar la acción requerida"
        )


# Endpoint que detalla un jugador en particular
# Recibe como parámetro el nombre del jugador


@app.get("/jugadores/{nombre_jugador}")
async def detalle_jugador(nombre_jugador: str):
    try:
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
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudo acceder a la información del jugador solicitado",
        )
