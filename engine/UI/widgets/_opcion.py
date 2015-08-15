from pygame import font, Rect
from .basewidget import BaseWidget
from engine.libs.render_tagged_text import render_tagged_text
from engine.libs.textrect import render_textrect

class _opcion (BaseWidget):
    '''Opción única que es parte de una lista más grande.
    No tiene cantidad, pero puede ser seleccionada (resaltando)
    mediante serElegido.'''
    tipo = 'fila'
    isSelected = False
    
    def __init__(self,texto,ancho,pos,fuente='verdana',size=16,aling=0,extra_data=None):
        self.pos = pos
        self.size = size
        self.fuente = font.SysFont(fuente, size)
        self.rect = Rect((-1,-1),(ancho,self.fuente.get_height()+1))
        self.aling = aling
        self.extra_data = extra_data
        
        self.setText(texto)
        super().__init__(self.img_uns)
        self.rect = self.img_uns.get_rect(topleft=self.pos)
        
    def setText(self,texto):
        '''Cambia y asigna el texto de la opción'''
        
        w,h = self.rect.size
        a = self.aling
        
        self.img_uns = render_tagged_text(texto,w,h,self.tags,bgcolor=self.bg_cnvs,justification=a)
        self.img_sel = render_tagged_text(texto,w,h,self.tags,bgcolor=self.font_low_color,justification=a)
                
        if self.isSelected: self.serElegido()
        else: self.serDeselegido()
        
        self.nombre = texto
    
    def __repr__(self):
        return self.nombre
