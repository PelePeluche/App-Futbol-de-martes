import pony.orm as pony
from datetime import date
from enum import IntEnum
from mixins import *


db = pony.Database()

# Definición de clase Jugador y sus atributos


class Jugador(db.Entity, JugadorMixin):
    id_jugador = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str)
    resultados = pony.Set("Resultado")
    partidos = pony.Set("Partido")
    equipos = pony.Set("Equipo", reverse="jugadores")
    capitan_de = pony.Set("Equipo", reverse="capitan")


# Definición de clase Equipo y sus atributos


class Equipo(db.Entity, EquipoMixin):
    id_equipo = pony.PrimaryKey(int, auto=True)
    partido = pony.Required("Partido")
    resultado = pony.Optional("Resultado")
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


# Definición de TAD Result


class Result(IntEnum):
    GANADO = 1
    EMPATADO = 2
    PERDIDO = 3


# Definición de clase Resultado y sus atributos


class Resultado(db.Entity, ResultadoMixin):
    id_resultado = pony.PrimaryKey(int, auto=True)
    resultado = pony.Required(Result, unique=True)
    equipos = pony.Set(Equipo)
    jugadores = pony.Set(Jugador)


# Line used for debugging
pony.set_sql_debug(True)

# Creation of tables for the models
db.bind("sqlite", "database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
