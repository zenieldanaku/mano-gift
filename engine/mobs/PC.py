from engine.globs.eventDispatcher import EventDispatcher
from .Inventory import Inventory, InventoryError
from .CompoMob import Parlante
from .mob import Mob


class PC(Mob, Parlante):
    
    def __init__(self, data, x, y, ):
        super().__init__(data, x, y, focus=True)
        self.inventario = Inventory(10, 10 + self.fuerza)

    # noinspection PyMethodOverriding
    def mover(self, dx, dy):
        self.moviendose = True
        self.animar_caminar()
        if dx > 0:
            self.cambiar_direccion('derecha')
        elif dx < -0:
            self.cambiar_direccion('izquierda')

        if dy < 0:
            self.cambiar_direccion('arriba')
        elif dy > 0:
            self.cambiar_direccion('abajo')

        dx, dy = dx * self.velocidad, dy * self.velocidad
        if not self.detectar_colisiones(dx, 0):
            self.reubicar(dx, 0)  # el heroe se mueve en el mapa, no en la camara
        if not self.detectar_colisiones(0, dy):
            self.reubicar(0, dy)
        
    def accion(self):
        x, y = self.direcciones[self.direccion]
        
        sprite = self._interact_with_mobs(x, y)
        if sprite is not None:
            if self.estado == 'cmb':
                self.atacando = True
                x, y = x * self.fuerza, y * self.fuerza
                self.atacar(sprite, x, y)
            else:
                return self.iniciar_dialogo(x, y)
        else:
            sprite = self._interact_with_props(x, y)
            if hasattr(sprite, 'accion'):
                if sprite.accion == 'agarrar':
                    try:
                        item = sprite()
                        self.inventario.agregar(item)
                        EventDispatcher.trigger('DelItem', self.tipo, {'obj': sprite})
                    except InventoryError as Error:
                        print(Error)

                elif sprite.accion == 'operar':
                    sprite.operar()

    def atacar(self, sprite, x, y):
        sprite.reubicar(x, y)
        sprite.recibir_danio(self.fuerza)

    def usar_item(self, item):
        if item.tipo == 'consumible':
            if item.usar(self):
                return self.inventario.remover(item)

    def cambiar_estado(self):
        if self.estado == 'idle':
            self.establecer_estado('cmb')

        elif self.estado == 'cmb':
            self.establecer_estado('idle')

        self.image = self.images['S' + self.direccion]
        self.mask = self.mascaras['S' + self.direccion]

        self.cambiar_direccion(self.direccion)
        self.animar_caminar()

    def update(self):
        self.moviendose = False
        if self.atacando:
            self.animar_ataque(5)
        
        super().update()

    def iniciar_dialogo(self, x, y):
        if x:
            if x > 0:
                post_dir = 'izquierda'
            else:
                post_dir = 'derecha'
        elif y:
            if y < 0:
                post_dir = 'abajo'
            else:
                post_dir = 'arriba'
        else:
            # esto nunca sucede; está por una correcion de PyCharm
            post_dir = ''

        sprite = self._interact_with_mobs(x, y)
        if sprite is not None:
            sprite.iniciar_dialogo(post_dir)

        return super().hablar(sprite)
