from pygame.sprite import LayeredDirty
from .constantes import Constants as C

class Renderer:
    camara = None
    overlays = None

    def __init__(self):
        self.camara = Camara()
        self.overlays = LayeredDirty()
    
    def clear(self):
        self.camara.contents.empty()
        self.overlays.empty()
    
    def setBackground(self,bg):
        self.camara.setBackground(bg)

    def addObj(self,obj,layer):
        self.camara.addFgObj(obj,layer)
    
    def update(self,fondo):
        fondo.fill((0,0,0))
        self.camara.update()
        self.overlays.update()
        ret = self.camara.draw(fondo) + self.overlays.draw(fondo)
        
        return ret
    
class Camara:
    bg = None # el fondo
    focus = None # objeto que la camara sigue.
    contents = None # objetos del frente
    
    def __init__(self):
        self.contents = LayeredDirty()
    
    def setBackground(self,spr):
        self.bg = spr
        self.contents.add(self.bg)
        #self.centrar()
    
    def addFgObj(self,spr,_layer=0):
        if spr not in self.contents:
            self.contents.add(spr,layer=_layer)
    
    def delObj(self,obj):
        if obj in self.contents:
            self.contents.remove(obj)
    
    def setFocus(self,spr):
        self.focus = spr
    
    def panear(self,dx,dy):
        newPos = self.bg.rect.x + dx
        if newPos > 0 or newPos < -(self.bg.rect.w - C.ANCHO) or self.focus.rect.x != self.focus.centroX:
            if C.ANCHO > self.focus.rect.x - dx  >=0:
                self.bg.rect.x = 0
        else:
            self.bg.rect.x += dx
                
        newPos = self.bg.rect.y + dy
        if newPos > 0 or newPos < -(self.bg.rect.h - C.ALTO) or self.focus.rect.y != self.focus.centroY:
            if C.ALTO > self.focus.rect.y - dy  >=0:
                self.bg.rect.y = 0
        else:
            self.bg.rect.y += dy

        for spr in self.contents:
            if spr != self.bg:
                self.contents.change_layer(spr, spr.rect.bottom)
                spr.dirty = 1
        
        self.centrar()
        self.bg.dirty = 1
        
    def centrar(self):
        self.focus.rect.x = int(C.ANCHO / C.CUADRO / 2) * C.CUADRO #224
        self.focus.rect.y = int(C.ALTO / C.CUADRO / 2) * C.CUADRO #224
        self.focus.centroX, self.focus.centroY = self.focus.rect.topleft

        newPosX = self.focus.rect.x - self.focus.mapX
        offsetX = C.ANCHO - newPosX - self.bg.rect.w
        if offsetX <= 0:
            if newPosX > 0:
                self.focus.rect.x -= newPosX
            else:
                self.bg.rect.x = newPosX
        else:
            self.bg.rect.x = newPosX+offsetX
            self.focus.rect.x += offsetX
        
        newPosY = self.focus.rect.y - self.focus.mapY
        offsetY = C.ALTO - newPosY - self.bg.rect.h
        if offsetY <= 0:
            if newPosY > 0:
                self.focus.rect.y -= newPosY
            else:
                self.bg.rect.y = newPosY
        else:
            self.bg.rect.y = newPosY+offsetY
            self.focus.rect.y += offsetY
        
        for spr in self.contents:
            if spr != self.focus and spr != self.bg:
                spr.rect.x = self.bg.rect.x + spr.mapX
                spr.rect.y = self.bg.rect.y + spr.mapY
            spr.dirty = 1
    
    def update(self):
        self.bg.update()
        self.contents.update()
    
    def draw(self,fondo):
        return self.contents.draw(fondo)
    