import pony.orm as pony
from datetime import date
from mixins import *


db = pony.Database()


class Jugador(db.Entity):
    id_jugador = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str)
    jugados = pony.Optional(int)
    puntos = pony.Optional(int)
    resultados = pony.Set("Resultado")
    partidos = pony.Set("Partido")
    equipos = pony.Set("Equipo", reverse="jugadores")
    capitan_de = pony.Set("Equipo", reverse="capitan")


class Equipo(db.Entity):
    id_equipo = pony.PrimaryKey(int, auto=True)
    partido = pony.Required("Partido")
    resultado = pony.Optional("Resultado")
    goles = pony.Optional(int)
    jugadores = pony.Set(Jugador, reverse="equipos")
    capitan = pony.Optional(Jugador, reverse="capitan_de")
    pechera = pony.Optional(str)


class Partido(db.Entity):
    id_partido = pony.PrimaryKey(int, auto=True)
    cancha = pony.Optional("Cancha")
    jugadores_anotados = pony.Set(Jugador)
    equipos = pony.Set(Equipo)
    fecha = pony.Optional(date)


class Cancha(db.Entity):
    id_cancha = pony.PrimaryKey(int, auto=True)
    nombre = pony.Optional(str)
    tamanio = pony.Optional(int)
    direccion = pony.Optional(str)
    partidos = pony.Set(Partido)


class Resultado(db.Entity):
    id_resultado = pony.PrimaryKey(int, auto=True)
    resultado = pony.Optional(str, unique=True)
    equipos = pony.Set(Equipo)
    jugadores = pony.Set(Jugador)


# Line used for debugging
pony.pony.Set_sql_debug(True)

# Creation of tables for the models
db.bind("sqlite", "database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
