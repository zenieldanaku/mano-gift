from engine.globs import EngineData as Ed
from .Inventory import Inventory, InventoryError
from .CompoMob import Parlante
from .mob import Mob


class PC(Mob, Parlante):
    alcance_cc = 0  # cuerpo a cuerpo.. 16 es la mitad de un cuadro.

    def __init__(self, data, x, y, ):
        super().__init__(data, x, y, focus=True)
        self.alcance_cc = data['alcance_cc']
        self.inventario = Inventory(10, 10 + self.fuerza)

    def mover(self, dx, dy):
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
        # DETECTAR LAS SALIDAS
        for spr in self.stage.salidas:
            if self.colisiona(spr, dx, dy):
                Ed.setear_mapa(spr.dest, spr.link)
                dx, dy = 0, 0

        if not self.detectar_colisiones(dx, 0):
            self.reubicar(dx, 0)  # el heroe se mueve en el mapa, no en la camara
        if not self.detectar_colisiones(0, dy):
            self.reubicar(0, dy)
        
    def accion(self):
        x, y = self.direcciones[self.direccion]

        if self.estado == 'cmb':
            # la animacion de ataque se hace siempre,
            # sino pareciera que no pasa nada
            self.atacando = True
            sprite = self._interact_with_mobs(x, y)
            if issubclass(sprite.__class__, Mob):
                if self.estado == 'cmb':
                    x, y = x * self.fuerza, y * self.fuerza
                    self.atacar(sprite, x, y)
        else:
            sprite = self._interact_with_props(x, y)
            if hasattr(sprite, 'accion'):
                if sprite.accion == 'agarrar':
                    try:
                        item = sprite()
                        self.inventario.agregar(item)
                        self.stage.del_property(sprite)
                    except InventoryError as Error:
                        print(Error)

                elif sprite.accion == 'operar':
                    sprite.operar()

    def atacar(self, sprite, x, y):
        sprite.reubicar(x, y)
        sprite.recibir_danio(self.fuerza)

    def recibir_danio(self, danio):
        super().recibir_danio(danio)
        if self.salud_act == 0:
            print('lanzar evento: muerte del heroe (y perdida de focus)')

    def usar_item(self, item):
        if item:
            if item.tipo == 'consumible':
                usado = item.usar(self)
                if usado:
                    return self.inventario.remover(item)
            return self.inventario.cantidad(item)
        else:
            return 0

    def cambiar_estado(self):
        if self.estado == 'idle':
            self.establecer_estado('cmb')

        elif self.estado == 'cmb':
            self.establecer_estado('idle')

        self.image = self.images['S' + self.direccion]
        # self.image = U.crear_sombra(t_image)
        # self.image.blit(t_image,[0,0])
        self.mask = self.mascaras['S' + self.direccion]

        self.cambiar_direccion(self.direccion)
        self.animar_caminar()

    def update(self):
        if self.atacando:
            self.animar_ataque(5)
        
        super().update()

    def iniciar_dialogo(self):
        x, y = self.direcciones[self.direccion]
        
        sprite = self._interact_with_mobs(x, y)
        post_dir = ''
        if x:
            if x > 0:
                post_dir = 'izquierda'
            else:
                post_dir = 'derecha'
        if y:
            if y < 0:
                post_dir = 'abajo'
            else:
                post_dir = 'arriba'
        
        if sprite is not None:
            sprite.iniciar_dialogo(self, post_dir)
        return super().hablar(sprite)
