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
    puntos = pony.Required(int, default=0)
    jugados = pony.Required(int, default=0)
    promedio = pony.Required(float, default=0)


# Función para crear un jugador


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
    jugado = pony.Required(bool, default=False)


# Definición de clase Cancha y sus atributos


class Cancha(db.Entity, CanchaMixin):
    id_cancha = pony.PrimaryKey(int, auto=True)
    nombre = pony.Optional(str)
    tamanio = pony.Optional(int)
    direccion = pony.Optional(str)
    partidos = pony.Set(Partido)


# Line used for debugging
pony.set_sql_debug(True)

# Creation of tables for the models
db.bind("sqlite", "database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

## Funciones de acceso a BDD


# Función para crear un jugador


@pony.db_session()
def crear_jugador(nombre_jugador):
    jugador = Jugador(nombre=nombre_jugador)
    return jugador


# Función para crear un partido


@pony.db_session()
def crear_partido():
    partido = Partido()
    return partido


# Función para obtener la lista de partidos


@pony.db_session()
def get_partidos():
    try:
        return db.Partido.select()
    except:
        raise HTTPException(status_code=500, detail="No se pudieron encontrar partidos")


# Función para detallar un partido en particular
# Recibe como parámetro el id del partido


@pony.db_session()
def get_partido_by_id(id_partido: int):
    try:
        return Partido[id_partido]
    except:
        raise HTTPException(status_code=500, detal="No existe el partido solicitado")


# Función que obtiene el id del próximo partido


@pony.db_session()
def get_id_proximo_partido():
    try:
        return len(db.Partido.select())
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo obtener el id del proximo partido"
        )


# Función que obtiene la lista de equipos de un partido en particular
# Recibe como parámetro el objeto Partido


@pony.db_session()
def get_lista_de_equipos_by_partido(partido: Partido):
    try:
        return partido.equipos.select()[:]
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los equipos del partido solicitado",
        )


# Función que obtiene la lista de jugadores anotados para un partido
# Recibe como parámetro el id del partido


@pony.db_session()
def get_lista_de_jugadores_anotados_by_partido_id(partido_id: int):
    try:
        partido = get_partido_by_id(partido_id)
        return partido.jugadores_anotados.select()[:]
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los jugadores anotados del partido solicitado",
        )


# Función que obtiene la lista de jugadores de un equipo para un partido
# Recibe como parámetro el objeto Partido y el número de equipo dentro del partido (1 o 2)


@pony.db_session()
def get_lista_de_jugadores_by_partido_by_equipo(partido: Partido, equipo_numero: int):
    try:
        return get_lista_de_equipos_by_partido(partido)[
            equipo_numero - 1
        ].jugadores.select()
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los jugadores del equipo solicitado",
        )


# Función que obtiene los goles marcados por un equipo en un partido en particular
# Recibe como parámetro el objeto Partido y el número de equipo dentro del partido (1 o 2)


@pony.db_session()
def get_goles_by_partido_by_equipo(partido: Partido, equipo_numero: int):
    try:
        return get_lista_de_equipos_by_partido(partido)[equipo_numero - 1].goles
    except:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener los goles del equipo solicitado",
        )


# Función que devuelve la lista de jugadores


@pony.db_session()
def get_jugadores():
    try:
        return db.Jugador.select()
    except:
        raise HTTPException(
            status_code=500, detail="No se pudieron encontrar jugadores"
        )


# Función que devuelve un jugador en particular dado su id
# Recibe como parámetro el id del jugador


@pony.db_session()
def get_jugador_by_id(id_jugador: int):
    try:
        return Jugador[id_jugador]
    except:
        raise HTTPException(
            status_code=500, detail="El jugador solicitado no fue encontrado"
        )


# Función que devuelve un jugador en particular dado su nombre
# Recibe como parámetro el nombre del jugador


@pony.db_session()
def get_jugador_by_nombre(nombre_jugador: str):
    try:
        return db.Jugador.select(lambda j: j.nombre == nombre_jugador).first()
    except:
        raise HTTPException(
            status_code=500, detail="El jugador solicitado no fue encontrado"
        )


# Función que obtiene la lista de equipos en los que jugaron juntos dos jugadores
# Recibe como parámetros los nombres de los dos jugadores


@pony.db_session()
def get_lista_equipos_juntos(nombre_jugador_1: str, nombre_jugador_2: str):
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


# Función que agrega un jugador al próximo partido
# Recibe como parámetro el nombre del jugador


@pony.db_session()
def agregar_jugador_a_proximo_partido(nombre_jugador: str):
    try:
        partido = get_partido_by_id(get_id_proximo_partido())
        jugador = get_jugador_by_nombre(nombre_jugador)
        partido.add_jugador(jugador)
        return partido
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo agregar el jugador al proximo partido"
        )


# Función que quita a un jugador del próximo partido
# Recibe como parámetro el nombre del jugador


@pony.db_session()
def quitar_jugador_de_proximo_partido(nombre_jugador: str):
    try:
        partido = get_partido_by_id(get_id_proximo_partido())
        jugador = get_jugador_by_nombre(nombre_jugador)
        partido.remove_jugador(jugador)
        return partido
    except:
        raise HTTPException(
            status_code=500, detail="No se pudo quitar al jugador del partido"
        )


# Función que obtiene la lista con jugadores que cumplen una mínima cantidad de partidos
# Recibe como parámetro la cantidad mínima de partidos


@pony.db_session()
def get_lista_jugadores_with_min_partidos(
    minimo_de_partidos: int, cantidad_de_jugadores: int
):
    try:
        return (
            db.Jugador.select(lambda j: len(j.resultados) >= minimo_de_partidos)
            .sort_by(pony.desc(Jugador.promedio))
            .limit(cantidad_de_jugadores)
        )

    except:
        raise HTTPException(
            status_code=500, detail="No se pudieron encontrar jugadores"
        )
