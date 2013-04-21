from pygame import sprite,mask,Surface
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C
from UI import Dialog

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    images = {} #incluye todas las imagenes del mob, arriba abajo izquierda y derecha
    direcciones = {'abajo':[0,1],'izquierda':[1,0],'arriba':[0,-1],'derecha':[-1,0],'ninguna':[0,0]}
    direccion = 'abajo'
    ticks,mov_ticks = 0,0
    AI = None # determina cómo se va a mover el mob
    modo_colision = None# determina qué direccion tomará el mob al chocar con algo
    start_pos = 0,0
    
    def __init__(self, ruta_img,stage,x=None,y=None,data = None):
        keys = 'abajo,derecha,arriba,izquierda'.split(',')
        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        for key in keys:
            self.images[key] = spritesheet[keys.index(key)]
        self.image = self.images[self.direccion]
        super().__init__(self.image,stage)
        
        if data != None:
            self.cambiar_direccion(directo=data['direccion'])
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
        
        if x != None and y != None:
            self.start_pos = x*C.CUADRO,y*C.CUADRO
            self.ubicar(*self.start_pos)

    def cambiar_direccion(self, directo = None, modo = 'usuario'):
        direccion = 'ninguna'
        
        if modo == 'random':
            lista = list(self.direcciones.keys())
            lista.remove(self.direccion)
            direccion = choice(lista)
        
        elif modo == 'contraria':
            if self.direccion == 'arriba':
                direccion = 'abajo'
            
            elif self.direccion == 'abajo':
                direccion = 'arriba'
            
            elif self.direccion == 'izquierda':
                direccion = 'derecha'
            
            elif self.direccion == 'derecha':
                direccion = 'izquierda'
        
        elif modo == 'usuario' and directo != None:
            direccion = directo
         
        if direccion != 'ninguna':
            self.image = self.images[direccion]
            self.mask = mask.from_surface(self.image,1)
        self.direccion = direccion
    
    def mover(self):
        if self.AI == None:
            self.ticks += 1
            self.mov_ticks += 1
            self._mover()
            if self.mov_ticks == 3:
                self.mov_ticks = 0
                pos = 10
                if randint(1,101) <= pos:
                    self.cambiar_direccion(self,modo='random')
        
        else:
            START = self.start_pos
            CURR_X = self.mapX
            CURR_Y = self.mapY
            
            modo = self.AI['modo']
            eje  = self.AI['eje']
            dist = self.AI['dist']
            
            if modo == 'Patrulla':
                if eje == 'x':
                    pA = START[0]-round(dist/2)
                    pB = START[0]+round(dist/2)

                    if CURR_X - self.velocidad <= pA or CURR_X + self.velocidad >= pB:
                        self.cambiar_direccion(self, modo=self.modo_colision)

                elif eje == 'y':
                    pA = START[1]-round(dist/2)
                    pB = START[1]+round(dist/2)
                    
                    if CURR_Y - self.velocidad <= pA or CURR_Y + self.velocidad >= pB:
                        self.cambiar_direccion(self, modo=self.modo_colision)
                    
                self._mover()
                                
    def _mover(self):
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad
        layers = [C.CAPA_GROUND_ITEMS,C.CAPA_GROUND_MOBS,C.CAPA_HERO]
        
        col_bordes = False #colision contra los bordes de la pantalla
        col_mobs = False #colision contra otros mobs
        col_heroe = False #colision contra el héroe
        col_items = False # colision contra los props
        col_mapa = False # colision contra las cajas de colision del propio mapa
        
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
            col_mapa = True
            #print(self.nombre+' colisiona con el mapa en X')
        
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
            col_mapa = True
            #print(self.nombre+' colisiona con el mapa en Y')
        
        for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if self.colisiona(spr,dx,dy) == True:
                col_items = True
                #print(self.nombre+' colisiona con '+str(spr.nombre))
                
        for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
            if self.colisiona(spr,dx,dy) == True:
                col_mobs = True
                #print(self.nombre+' colisiona con '+str(spr.nombre))
                
        for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_HERO):
            if self.colisiona(spr,dx,dy) == True:
                col_heroe = True
                #print(self.nombre+' colisiona con '+str(spr.nombre))
        
        newPos = self.mapX + dx
        if newPos < 0 or newPos > self.stage.mapa.rect.w:
            if C.ANCHO > self.rect.x - dx  >=0:
                col_bordes = True
                #print(self.nombre+' colisiona con borde horizontal')
        
        newPos = self.mapY + dy
        if newPos < 0 or newPos > self.stage.mapa.rect.h:
            if C.ALTO > self.rect.y - dy  >=0:
                col_bordes = True
                #print(self.nombre+' colisiona con borde vertical')
        
        colisiones = [col_bordes,col_mobs,col_items,col_mapa,col_heroe]
        if any(colisiones):
            self.cambiar_direccion(self,modo=self.modo_colision)
        
            x,y = self.direcciones[self.direccion]
            dx,dy = x*self.velocidad,y*self.velocidad
        
        self.reubicar(dx, dy)

class PC (Mob):
    centroX = 0
    centroY = 0
    def __init__(self,nombre,ruta_imgs,stage):
        self.direccion = 'abajo'
        super().__init__(ruta_imgs,stage)
        self.nombre = nombre
        
    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.dirty = 1
    
    def accion(self):
        actuar = False
        rango = 15
        for mob in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):                    
            if self.direccion == 'arriba':
                if self.colisiona(mob,0,-1*rango):
                    actuar = True
                    objetivo = mob
            elif self.direccion == 'abajo':
                if self.colisiona(mob,0,+1*rango):
                    actuar = True
                    objetivo = mob
            elif self.direccion == 'derecha':
                if self.colisiona(mob,-1*rango,0):
                    actuar = True
                    objetivo = mob
            elif self.direccion == 'izquierda':
                if self.colisiona(mob,+1*rango,0):
                    actuar = True
                    objetivo = mob
            
        if actuar == True:
            if isinstance(objetivo,Enemy):
                objetivo.morir()
        
            elif isinstance(objetivo,NPC):
                objetivo.interactuar()
    
    def atacar(self):
        pass

class NPC (Mob):
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
    
    def interactuar(self):
        texto = Dialog('hola, heroe!')
        self.stage.contents.add(texto, layer=texto.layer)

class Enemy (Mob):
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
    
    def morir(self):
        self.stage.contents.remove(self)
        print('Mob '+self.nombre+' eliminado!')
  
class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass