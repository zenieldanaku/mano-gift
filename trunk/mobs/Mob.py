import sys
from pygame import mask,time
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C, Tiempo as T
from mobs.MobGroup import MobGroup
from .Vision import area_vision

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    images = {} #incluye todas las imagenes del mob, arriba abajo izquierda y derecha
    death_img = None #sprite del mob muerto.
    dead = False
    direcciones = {'abajo':[0,1],'izquierda':[1,0],'arriba':[0,-1],'derecha':[-1,0],'ninguna':[0,0]}
    direccion = 'abajo'
    ticks,mov_ticks = 0,0
    AI = None # determina cómo se va a mover el mob
    modo_colision = None# determina qué direccion tomará el mob al chocar con algo
    patrol_p = []
    next_p = 0
    vision = None
    cuenta = -1
    show = {}
    hide = {}
    
    def __init__(self, ruta_img,stage,x=None,y=None,data = None):
        maskeys=['S'+'abajo','S'+'arriba','S'+'derecha','S'+'izquierda',
                 'I'+'abajo','I'+'arriba','I'+'derecha','I'+'izquierda',
                 'D'+'abajo','D'+'arriba','D'+'derecha','D'+'izquierda']

        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        self.patrol_p = []
        self.generar_rasgos()
        for key in maskeys:
            self.images[key] = spritesheet[maskeys.index(key)]
        self.image = self.images['Sabajo']
        super().__init__(self.image,stage)

        if data != None:
            self.cambiar_direccion(data['direccion'])
            self.vision = area_vision(self.direccion)
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
            self.salud = data['salud']
            self.actitud = data['actitud']
            if 'solido' in data:
                self.solido = data['solido']
            #eliminar esto una vez que esté aplicado a todos los mobs
            if 'death' in data:
                self.death_img = r.cargar_imagen(data['death'])

        if x != None and y != None:
            self.ubicar(x*C.CUADRO,y*C.CUADRO)
            if type(self.AI) == dict:
                for punto in self.AI['seq']:
                    dx,dy = self.AI['puntos'][punto]
                    dx += x*C.CUADRO
                    dy += y*C.CUADRO
                    self.patrol_p.append([dx,dy])
                self.AI = 'patrol'
        
    def generar_rasgos(self):
        rasgos = r.abrir_json('scripts/rasgos.json')
        
        for car in rasgos['cars']:
            if rasgos['cars'][car]:
                self.show[car] = {"tipo": "atributo", "nombre":car, "value": 0}
            else:
                self.hide[car] = {"tipo": "atributo", "nombre":car, "value": 0}
        
        for hab in rasgos['habs']:
            if rasgos['habs'][hab]:
                self.show[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}
            else:
                self.hide[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}
                
        #print(self.nombre)
        #for car in self.cars:
        #    if self.cars[car]['show']:
        #        print(car, self.cars[car]["value"])
        #for hab in self.habs:
        #    if self.habs[hab]['show']:
        #        print(hab, self.habs[hab]["value"])
        #print()
                    
    def _determinar_direccion(self,curr_p,next_p):
        pX,pY = curr_p
        nX,nY = next_p
        
        dx = pX-nX
        dy = pY-nY
        
        if dx > dy:
            if dy < 0:
                direccion = 'abajo'
            else:
                direccion = 'derecha'
        else:
            if dx < 0:
                direccion = 'izquierda'
            else:
                direccion = 'arriba'
        
        return direccion
    
    def cambiar_direccion(self,arg=None):
        direccion = 'ninguna'

        if arg == None:
            if self.AI == 'wanderer':
                lista = list(self.direcciones.keys())
                lista.remove(self.direccion)
                direccion = choice(lista)

            elif self.AI == 'patrol':
                curr_p = [self.mapX,self.mapY]    
                direccion = self._determinar_direccion(curr_p,self.patrol_p[self.next_p])
            
        elif arg == 'contraria':
            if self.direccion == 'arriba': direccion = 'abajo'
            elif self.direccion == 'abajo': direccion = 'arriba'
            elif self.direccion == 'izquierda': direccion = 'derecha'
            elif self.direccion == 'derecha': direccion = 'izquierda'

        elif arg in self.direcciones:
            direccion = arg
            
        self.direccion = direccion
        return direccion
        
    def animar_caminar(self):
        '''cambia la orientación del sprite y controla parte de la animación'''
        
        for key in self.images.keys():
            if self.image == self.images[key]:
                break
        self.timer_animacion += T.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if key == 'D'+self.direccion:
                self.image = self.images['I'+self.direccion]
            elif key == 'I'+self.direccion:
                self.image = self.images['D'+self.direccion]
            elif self.direccion == 'ninguna':
                pass
            else:
                self.image = self.images['D'+self.direccion]
    
    def mover(self):
        if self.AI == "wanderer":
            self.ticks += 1
            self.mov_ticks += 1
            direccion = self.direccion
            if self.mov_ticks == 3:
                self.mov_ticks = 0
                pos = 10
                if randint(1,101) <= pos:
                    direccion = self.cambiar_direccion()
        
        elif self.AI == 'patrol':
            curr_p = [self.mapX,self.mapY]
            if curr_p == self.patrol_p[self.next_p]:
                self.next_p += 1
                if self.next_p >= len(self.patrol_p):
                    self.next_p = 0
            punto_proximo = self.patrol_p[self.next_p]
            
            direccion = self._determinar_direccion(curr_p,punto_proximo)
            self.cambiar_direccion(direccion)
        
        self.vision.cambiar_direccion(direccion)
        self._mover()
                
    def _mover(self):
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad

        col_bordes = False #colision contra los bordes de la pantalla
        col_mobs = False #colision contra otros mobs
        col_heroe = False #colision contra el héroe
        col_items = False # colision contra los props
        col_mapa = False # colision contra las cajas de colision del propio mapa

        if self.solido:
            if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
                col_mapa = True

            if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
                col_mapa = True

            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
                if self.colisiona(spr,dx,dy):
                    col_items = True
            
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
                if spr.solido:
                    if self.colisiona(spr,dx,dy):
                        col_mobs = True
                        
        if self.colisiona(W.HERO,dx,dy):
            col_heroe = True
            if self.actitud == 'hostil':
                self.atacar()

        newPos = self.mapX + dx
        if newPos < 0 or newPos > self.stage.mapa.rect.w:
            if C.ANCHO > self.rect.x - dx  >=0:
                col_bordes = True

        newPos = self.mapY + dy
        if newPos < 0 or newPos > self.stage.mapa.rect.h:
            if C.ALTO > self.rect.y - dy  >=0:
                col_bordes = True

        colisiones = [col_bordes,col_mobs,col_items,col_mapa,col_heroe]
        if any(colisiones):
            self.cambiar_direccion(self.modo_colision)

            x,y = self.direcciones[self.direccion]
            dx,dy = x*self.velocidad,y*self.velocidad
        
        self.animar_caminar()
        self.reubicar(dx, dy)
    
    def recibir_danio(self):
        self.salud -= 1
        
        if self.salud <= 0:
            if self.death_img != None:
                self.image = self.death_img
            else: # esto queda hasta que haga sprites 'muertos' de los npcs
                self.stage.contents.remove(self)
            self.dead = True
            MobGroup.removeMob(self)
    
    def ver(self):
        for spr in MobGroup.mobs:
            if MobGroup.mobs[spr] != self:
                spr = MobGroup.mobs[spr]
                v = self.vision
                if v.mask.overlap(spr.mask,(spr.mapX - v.x(self),
                                            spr.mapY - v.y(self))):
                                        
                    #self.cuenta += 1
                    #print(self.nombre,'ve a',spr.nombre,'(',str(self.cuenta),')')
                    #self.cambiar_direccion('contraria')
                    pass
                    

    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not W.onPause and not self.dead:
            self.mover()
            self.ver()