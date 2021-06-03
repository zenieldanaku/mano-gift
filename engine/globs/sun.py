from .event_dispatcher import EventDispatcher
from .game_groups import Mob_Group


class Sun:
    light = None
    lights = None

    @classmethod
    def init(cls, latitude):
        noroeste = 0
        suroeste = 2
        sureste = 4
        noreste = 6
        if latitude >= 0:  # el ">=" es porque las sombras este y oeste no andan bien
            # latitud norte
            cls.lights = [suroeste, 8, sureste]  # Puede que esto,
        elif latitude < 0:
            # latitud sur
            cls.lights = [noroeste, 8, noreste]  # esté al revés.

        EventDispatcher.register(cls.set_by_event, 'ClockAlarm')

    @classmethod
    def calculate(cls, actual, amanece, mediodia, atardece, anochece):
        alarm = None
        if amanece < actual < mediodia:  # mañana
            alarm = 'amanece'
        elif mediodia < actual < atardece:  # dia
            alarm = 'mediodía'
        elif atardece < actual < anochece:  # tarde noche
            alarm = 'atardece'
        elif anochece < actual or actual < amanece:  # noche
            alarm = 'anochece'

        cls.set_light(alarm)

    @classmethod
    def set_by_event(cls, event):
        alarm = event.data['time']
        cls.set_light(alarm)

    @classmethod
    def set_light(cls, alarm):
        if alarm == 'amanece':
            cls.light = cls.lights[0]
        elif alarm == 'mediodía':
            cls.light = cls.lights[1]  # overhead light.
        elif alarm == 'atardece':
            cls.light = cls.lights[2]
        elif alarm == 'anochece':
            cls.light = None

        for mob in Mob_Group:
            mob.recibir_luz_solar(cls.light)