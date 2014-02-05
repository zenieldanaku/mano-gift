from base import _giftSprite
from UI.estilo import Estilo
from pygame import Surface,Rect

class BaseWidget(Estilo,_giftSprite):
    enabled = True
    canvas = None
    
    def __init__(self,img):
        super().__init__(img)
    
    def serElegido(self):
        '''Cambia la imagen a la versión resaltada'''
        self.image = self.img_sel
        self.isSelected = True
        self.dirty = 1
        
    def serDeselegido(self):
        '''Cambia la imagen a la versión no elegida'''
        
        self.image = self.img_uns
        self.isSelected = False
        self.dirty = 1
    
    def crear_canvas(self,ancho,alto):
        canvas = Surface((ancho,alto))
        
        clip = Rect(0,0,ancho, alto)
        canvas.fill(self.bg_bisel_bg,rect=clip)
        
        clip = Rect(3,3,ancho, alto)
        canvas.fill(self.bg_bisel_fg,rect=clip)
        
        clip = Rect(3,3,ancho-7, alto-7)
        canvas.fill(self.bg_cnvs,rect=clip)
        
        return canvas
    
    def crear_inverted_canvas (self,ancho,alto):
        canvas = Surface((ancho, alto))
        
        clip = Rect(0,0,ancho, alto)
        canvas.fill(self.bg_bisel_fg,rect=clip)
        
        clip = Rect(3,3,ancho, alto)
        canvas.fill(self.bg_bisel_bg,rect=clip)
        
        clip = Rect(3,3,ancho-7, alto-7)
        canvas.fill(self.bg_cnvs,rect=clip)
        
        return canvas