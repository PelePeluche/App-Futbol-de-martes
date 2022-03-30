from models import *
from datos import datos


@pony.db_session()
def carga_datos():
    ganado = Resultado(resultado=1)
    empatado = Resultado(resultado=2)
    perdido = Resultado(resultado=3)

    for partido in datos:
        p = Partido()
        pony.commit()
        print(partido)

        jugadores_1 = datos[partido]["Equipo 1"]["jugadores"]
        print(jugadores_1)
        goles_1 = datos[partido]["Equipo 1"]["goles"]
        print(goles_1)
        e1 = Equipo(partido=p, goles=goles_1)
        p.add_equipo(e1)
        pony.commit()

        jugadores_2 = datos[partido]["Equipo 2"]["jugadores"]
        print(jugadores_2)
        goles_2 = datos[partido]["Equipo 2"]["goles"]
        print(goles_2)
        e2 = Equipo(partido=p, goles=goles_2)
        p.add_equipo(e2)
        pony.commit()

        if goles_1 > goles_2:
            e1.set_resultado(ganado)
            e2.set_resultado(perdido)
        elif goles_2 > goles_1:
            e1.set_resultado(perdido)
            e2.set_resultado(ganado)
        else:
            e1.set_resultado(empatado)
            e2.set_resultado(empatado)

        for jugador in jugadores_1:
            try:
                j = Jugador(nombre=jugador)
            except:
                j = db.Jugador.select(lambda j: j.nombre == jugador)[:][0]
                print(j)
            e1.add_jugador(j)
            j.add_resultado(e1.resultado)

        for jugador in jugadores_2:
            try:
                j = Jugador(nombre=jugador)
            except:
                j = db.Jugador.select(lambda j: j.nombre == jugador)[:][0]
                print(j)
            e1.add_jugador(j)
            j.add_resultado(e1.resultado)
