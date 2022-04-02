from fastapi import HTTPException
import pony.orm as pony
from datetime import date
from mixins import *


db = pony.Database()


# Definición de clase Jugador y sus atributos


class Jugador(db.Entity, JugadorMixin):
    id_jugador = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str, unique=True)
    resultados = pony.Optional(pony.IntArray)
    partidos = pony.Set("Partido")
    equipos = pony.Set("Equipo", reverse="jugadores")
    capitan_de = pony.Set("Equipo", reverse="capitan")


# Definición de clase Equipo y sus atributos


class Equipo(db.Entity, EquipoMixin):
    id_equipo = pony.PrimaryKey(int, auto=True)
    partido = pony.Required("Partido")
    resultado = pony.Optional(int)
    goles = pony.Optional(int)
    jugadores = pony.Set(Jugador, reverse="equipos")
    capitan = pony.Optional(Jugador, reverse="capitan_de")
    pechera = pony.Optional(str)


# Definición de clase Partido y sus atributos


class Partido(db.Entity, PartidoMixin):
    id_partido = pony.PrimaryKey(int, auto=True)
    cancha = pony.Optional("Cancha")
    jugadores_anotados = pony.Set(Jugador)
    equipos = pony.Set(Equipo)
    fecha = pony.Optional(date)


# Definición de clase Cancha y sus atributos


class Cancha(db.Entity, CanchaMixin):
    id_cancha = pony.PrimaryKey(int, auto=True)
    nombre = pony.Optional(str)
    tamanio = pony.Optional(int)
    direccion = pony.Optional(str)
    partidos = pony.Set(Partido)


# Definición de clase Resultado y sus atributos

"""
class Resultado(db.Entity, ResultadoMixin):
    id_resultado = pony.PrimaryKey(int, auto=True)
    resultado = pony.Required(Result, unique=True)
    equipos = pony.Set(Equipo)
    jugadores = pony.Set(Jugador)
"""

# Line used for debugging
pony.set_sql_debug(True)

# Creation of tables for the models
db.bind("sqlite", "database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

# Funciones de acceso a BDD


@pony.db_session()
def get_partidos():
    try:
        return db.Partido.select()
    except:
        raise HTTPException(
            status_code=500, detail="No se puddieron encontrar partidos"
        )


@pony.db_session()
def get_partido_by_id(id_partido):
    try:
        return Partido[id_partido]
    except:
        raise HTTPException(status_code=500, detal="No existe el partido solicitado")


@pony.db_session()
def get_lista_de_equipos_by_partido(partido):
    try:
        return partido.equipos.select()[:]
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los equipos del partido solicitado",
        )


@pony.db_session()
def get_lista_de_jugadores_by_partido_by_equipo(partido, equipo_numero):
    try:
        return get_lista_de_equipos_by_partido(partido)[
            equipo_numero - 1
        ].jugadores.select()
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los jugadores del equipo solicitado",
        )


@pony.db_session()
def get_goles_by_partido_by_equipo(partido, equipo_numero):
    try:
        return get_lista_de_equipos_by_partido(partido)[equipo_numero - 1].goles
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los goles del equipo solicitado",
        )


@pony.db_session()
def get_jugadores():
    try:
        return db.Jugador.select()
    except:
        raise HTTPException(
            status_code=500, detail="No se pudieron encontrar jugadores"
        )
