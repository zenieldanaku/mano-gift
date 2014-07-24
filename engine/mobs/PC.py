from engine.globs import Constants as C, Tiempo as T, MobGroup, EngineData as ED
from .Inventory import Inventory, InventoryError
from engine.mobs.scripts.dialogo import Dialogo
from pygame import Surface,Rect,mask
from engine.misc import Util as U
from .CompoMob import Parlante
from .mob import Mob

class PC(Mob,Parlante):   
    alcance_cc = 0 #cuerpo a cuerpo.. 16 es la mitad de un cuadro.
    atk_counter = 0
    atk_img_index = -1
    
    dx,dy = 0,0
    def __init__(self,data,x,y):
        super().__init__(data,x,y)
        self.alcance_cc = data['alcance_cc']
        self.inventario = Inventory(10,10+self.fuerza)
    
    def mover(self,dx,dy):
        
        self.animar_caminar()
        if dx > 0: self.cambiar_direccion('derecha')
        elif dx < -0: self.cambiar_direccion('izquierda')
        
        if dy < 0: self.cambiar_direccion('arriba')
        elif dy > 0: self.cambiar_direccion('abajo')
        
        dx,dy = dx*self.velocidad,dy*self.velocidad
        
        # DETECTAR LAS SALIDAS
        for spr in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_SALIDAS):
            if self.colisiona(spr,dx,dy):
                ED.setear_mapa(spr.dest,spr.link)
                dx,dy = 0,0
        
        if not self.detectar_colisiones(dx,0):
            self.reubicar(dx,0) # el heroe se mueve en el mapa, no en la camara
        if not self.detectar_colisiones(0,dy):
            self.reubicar(0,dy)

        
 
        self.dx,self.dy = -dx,-dy
        
    def accion(self):
        x,y = self.direcciones[self.direccion]
        
        if self.estado == 'cmb':
            # la animacion de ataque se hace siempre,
            # sino pareciera que no pasa nada
            self.atacando = True
            sprite = self._interactuar_mobs(self.alcance_cc)
            if issubclass(sprite.__class__,Mob):
                if self.estado == 'cmb':
                    x,y = x*self.fuerza,y*self.fuerza
                    self.atacar(sprite,x,y)
        else:
            sprite = self._interactuar_props(x,y)
            if hasattr(sprite,'accion'):
                if sprite.accion == 'agarrar':
                    try:
                        item = sprite()
                        self.inventario.agregar(item)
                        self.stage.delProperty(sprite)
                        ED.RENDERER.camara.delObj(sprite)
                    except InventoryError as Error:
                        print(Error)
                
                elif sprite.accion == 'operar':
                    sprite.operar()
    
    def atacar(self,sprite,x,y):
        sprite.reubicar(x,y)
        sprite.recibir_danio()
    
    def recibir_danio(self):
        super().recibir_danio()
        if self.salud == 0:
            print('lanzar evento: muerte del heroe (y perdida de focus)')
    
    def _anim_atk (self,limite):
        # construir la animación
        frames,alphas = [],[]
        for L in ['A','B','C']:
            frames.append(self.cmb_atk_img[L+self.direccion])
            alphas.append(self.cmb_atk_alpha[L+self.direccion])
            
        # iniciar la animación
        self.atk_counter += 1
        if self.atk_counter > limite:
            self.atk_counter = 0
            self.atk_img_index += 1
            if self.atk_img_index > len(frames)-1:
                self.atk_img_index = 0
                self.atacando = False
            
            self.image = frames[self.atk_img_index]
            #self.mask = self.cmb_walk_alpha['S'+self.direccion]
            self.mask = alphas[self.atk_img_index]
            #self.calcular_sombra(frames[self.atk_img_index])
    
    def hablar(self):
        sprite = self._interactuar_mobs(self.alcance_cc)
        if sprite != None:
            if sprite.hablante:
                self.interlocutor = sprite
                self.interlocutor.responder()
                ED.DIALOG = Dialogo(self,self.interlocutor)
                return True
        return False
    
    def _interactuar_mobs(self,rango):
        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for mob in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
            if mob != self:
                if self.colisiona(mob,x,y):
                    return mob
    
    def _interactuar_props(self,x,y):
        "Utiliza una máscara propia para seleccionar mejor a los props"
        self_mask = mask.Mask((32,32))
        self_mask.fill()
        dx,dy = x*32,y*32
    
        for prop in self.stage.interactives:
            x = prop.mapX-(self.mapX+dx)
            y = prop.mapY-(self.mapY+dy)
            if prop.image != None:
                prop_mask = mask.from_surface(prop.image)
                if prop_mask.overlap(self_mask,(-x,-y)):
                    return prop

    def ver_inventario(self):
        ED.DIALOG = Inventario_rapido()
    
    def usar_item (self,item):
        if item.tipo == 'consumible':
            print('Used',item.nombre) #acá iria el efecto del item utilizado.
            return self.inventario.remover(item)
        return self.inventario.cantidad(item)
            
    def cambiar_estado(self):
        if self.estado == 'idle':
            self.establecer_estado('cmb')
            
        elif self.estado == 'cmb':
            self.establecer_estado('idle')
            
        self.image = self.images['S'+self.direccion]
        #self.image = U.crear_sombra(t_image)
        #self.image.blit(t_image,[0,0])
        self.mask = self.mascaras['S'+self.direccion]
            
        self.cambiar_direccion(self.direccion)
        self.animar_caminar()
    
    def update(self):
        if self.atacando:
            self._anim_atk(5)
        dx,dy = self.dx,self.dy
        self.dx,self.dy = 0,0
        self.dirty = 1
        if (dx,dy) != (0,0):
            return dx,dy
