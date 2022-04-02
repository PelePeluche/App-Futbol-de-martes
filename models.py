from audioop import reverse
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
    partidos = pony.Set("Partido", reverse="jugadores_anotados")
    equipos = pony.Set("Equipo", reverse="jugadores")
    capitan_de = pony.Set("Equipo", reverse="capitan")


def crear_jugador(nombre_jugador):
    jugador = Jugador(nombre=nombre_jugador)
    pony.commit()
    return jugador


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
    jugadores_anotados = pony.Set(Jugador, reverse="partidos")
    equipos = pony.Set(Equipo)
    fecha = pony.Optional(date)


def crear_partido():
    partido = Partido()
    pony.commit()
    return partido


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
        raise HTTPException(status_code=500, detail="No se pudieron encontrar partidos")


@pony.db_session()
def get_partido_by_id(id_partido):
    try:
        return Partido[id_partido]
    except:
        raise HTTPException(status_code=500, detal="No existe el partido solicitado")


@pony.db_session()
def get_id_proximo_partido():
    try:
        return len(db.Partido.select())
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo obtener el id del proximo partido"
        )


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
def get_lista_de_jugadores_anotados_by_partido_id(partido_id):
    try:
        partido = get_partido_by_id(partido_id)
        return partido.jugadores_anotados.select()[:]
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los jugadores anotados del partido solicitado",
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


@pony.db_session()
def get_jugador_by_id(id_jugador):
    try:
        return Jugador[id_jugador]
    except:
        raise HTTPException(
            status_code=500, detail="El jugador solicitado no fue encontrado"
        )


@pony.db_session()
def get_jugador_by_nombre(nombre_jugador):
    try:
        return db.Jugador.select(lambda j: j.nombre == nombre_jugador).first()
    except:
        raise HTTPException(
            status_code=500, detail="El jugador solicitado no fue encontrado"
        )


@pony.db_session()
def get_lista_equipos_juntos(nombre_jugador_1, nombre_jugador_2):
    try:
        jugador_1 = db.Jugador.select(lambda j: j.nombre == nombre_jugador_1).first()
        jugador_2 = db.Jugador.select(lambda j: j.nombre == nombre_jugador_2).first()
        equipos_juntos = db.Equipo.select(
            lambda e: jugador_1 in e.jugadores and jugador_2 in e.jugadores
        )[:]
        return equipos_juntos
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron encontrar equipos en los que hayan jugado juntos",
        )
