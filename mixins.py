import pony.orm as pony


# Mixins para Jugador


class JugadorMixin(object):
    def set_nombre(self, nombre):
        self.nombre = nombre
        pony.commit()

    def add_resultado(self, resultado):
        self.resultados.append(resultado)
        pony.commit()

    def add_partido(self, partido):
        self.partidos.add(partido)
        pony.commit()

    def add_equipo(self, equipo):
        self.equipos.add(equipo)
        pony.commit()

    def add_capitan_de(self, equipo):
        self.capitan_de(equipo)
        pony.commit()

    def get_jugados(self):
        return len(self.resultados)

    def get_puntos(self):
        puntos = 0
        for r in self.resultados:
            puntos += r
        return puntos

    def get_resultados(self):
        ganados = 0
        empatados = 0
        perdidos = 0
        for r in self.resultados:
            if r == 3:
                ganados += 1
            elif r == 1:
                empatados += 1
            else:
                perdidos += 1
        return {
            "ganados": ganados,
            "empatados": empatados,
            "perdidos": perdidos,
        }

    def get_promedio(self):
        try:
            return self.get_puntos() / self.get_jugados()
        except ZeroDivisionError:
            print("No se puede calcular el promedio de ese gil")


# Mixins para Equipo


class EquipoMixin(object):
    def set_partido(self, partido):
        self.partido = partido
        pony.commit()

    def set_resultado(self, resultado):
        self.resultado = resultado
        pony.commit()

    def set_goles(self, goles):
        self.goles = goles
        pony.commit()

    def add_jugador(self, jugador):
        self.jugadores.add(jugador)
        pony.commit()

    def set_capitan(self, jugador):
        self.capitan = jugador
        pony.commit()

    def set_pechera(self, pechera):
        self.pechera = pechera
        pony.commit()


# Mixins para Partido


class PartidoMixin(object):
    def set_cancha(self, cancha):
        self.cancha = cancha
        pony.commit()

    def add_jugador(self, jugador):
        self.jugadores_anotados.add(jugador)
        pony.commit()

    def remove_jugador(self, jugador):
        self.jugadores_anotados.remove(jugador)
        pony.commit()

    def add_equipo(self, equipo):
        self.equipos.add(equipo)
        pony.commit()

    def set_fecha(self, fecha):
        self.fecha = fecha
        pony.commit()


# Mixins para Cancha


class CanchaMixin(object):
    def set_nombre(self, nombre):
        self.nombre = nombre
        pony.commit()

    def set_tamanio(self, tamanio):
        self.tamanio = tamanio
        pony.commit()

    def set_direccion(self, direccion):
        self.direccion = direccion
        pony.commit()

    def add_partido(self, partido):
        self.jugadores_anotados.add(partido)
        pony.commit()
