from engine.globs.event_aware import EventAware
from .CompoMob import Parlante
from .mob import Mob


class PC(EventAware, Parlante, Mob):

    def __init__(self, data, x, y):
        super().__init__(data, x, y, focus=True)
        self.functions['tap'].update({'accion': self.accion})

    # noinspection PyMethodOverriding
    def mover(self, direccion):
        if direccion != self.direccion:
            self.cambiar_direccion(direccion)
        if not self.detectar_colisiones():
            super().mover()

    def accion(self):
        super().accion()
        sprite = self.quadrant_interaction()
        if sprite is not None:
            if sprite.tipo == 'Mob':
                if self.estado == 'cmb':
                    self.atacar(sprite)
                else:
                    self.elegir_tema(sprite)
                    self.deregister()

            elif sprite.tipo == 'Prop':
                if sprite.action is not None:
                    sprite.action(self)

                elif self.estado != 'cmb':
                    sprite.show_description()
                    self.deregister()

    def cambiar_estado(self):
        super().cambiar_estado()
        self.register()
