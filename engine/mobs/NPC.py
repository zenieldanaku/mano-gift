from .CompoMob import Autonomo, Parlante
from .mob import Mob


class NPC(Parlante, Autonomo, Mob):
    hablando = False
    hablante = True

    def __init__(self, nombre, x, y, data):
        self.nombre = nombre
        super().__init__(data, x, y)

    def mover(self):
        if not self.hablando:
            super().mover()

    def update(self):
        if not self.hablando:
            super().update()
