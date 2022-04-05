from models import *
from datos import datos

# Funcion que carga datos de archivo .py con la forma datos={
#   "Partido 1": {
#       "Equipo 1": {
#           "jugadores": {},
#           "goles": },
#      "Equipo 2": {
#           "jugadores": {},
#           "goles": }
#      }
#    }


@pony.db_session()
def carga_datos():

    for partido in datos:
        p = Partido(jugado=True)
        pony.commit()
        print(partido)

        jugadores_1 = datos[partido]["Equipo 1"]["jugadores"]

        goles_1 = datos[partido]["Equipo 1"]["goles"]

        e1 = Equipo(partido=p, goles=goles_1)
        p.add_equipo(e1)
        pony.commit()

        jugadores_2 = datos[partido]["Equipo 2"]["jugadores"]

        goles_2 = datos[partido]["Equipo 2"]["goles"]

        e2 = Equipo(partido=p, goles=goles_2)
        p.add_equipo(e2)
        pony.commit()

        if goles_1 > goles_2:
            e1.set_resultado(3)
            e2.set_resultado(0)
        elif goles_2 > goles_1:
            e1.set_resultado(0)
            e2.set_resultado(3)
        else:
            e1.set_resultado(1)
            e2.set_resultado(1)

        for jugador in jugadores_1:
            try:
                j = Jugador(nombre=jugador, resultados=[])
            except:
                j = db.Jugador.select(nombre=jugador)[:][0]

            e1.add_jugador(j)
            j.add_resultado(e1.resultado)
            print(p.add_jugador(j))
            j.increase_jugados()
            j.increase_puntos(e1.resultado)
            j.actualize_promedio()

        for jugador in jugadores_2:
            try:
                j = Jugador(nombre=jugador, resultados=[])
            except:
                j = db.Jugador.select(nombre=jugador)[:][0]

            e2.add_jugador(j)
            j.add_resultado(e2.resultado)
            print(p.add_jugador(j))
            j.increase_jugados()
            j.increase_puntos(e2.resultado)
            j.actualize_promedio()
