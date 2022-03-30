import pony.orm as pony


# Mixins para Jugador


class JugadorMixin(object):
    def set_nombre(self, nombre):
        self.nombre = nombre
        pony.commit()

    def add_resultado(self, resultado):
        self.resultados.add(resultado)
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
            if r.resultado == 1:
                puntos += 3
            elif r.resultado == 2:
                puntos += 1
        return puntos


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


# Mixin para Resultado


class ResultadoMixin(object):
    def set_resultado(self, resultado):
        self.resultado = resultado
        pony.commit()

    def add_equipo(self, equipo):
        self.equipo.add(equipo)
        pony.commit()

    def add_jugador(self, jugador):
        self.jugadores.add(jugador)
        pony.commit()
