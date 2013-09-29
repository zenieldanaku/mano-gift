# intro.py
# módulo de introducción y selección de modo.
from pygame import Surface, Rect, QUIT, KEYDOWN, KEYUP, sprite
from pygame import display as pantalla, event as EVENT,quit as py_quit,font
from globs import Tiempo as T, Constants as C, World as W
from misc import Resources as r
from UI import Menu_Inventario
from libs.textrect import render_textrect
import sys,os,os.path

# tiene una duración
# es previo al mainloop
# comienza con un cuadro negro
# aparece (fundido) el logo (o el titulo) Virtual Interactive
# presenta... (o en inglés, presents...)
# un juego de Lúdica Squamata
# a Ludica Squamata game
# ...
# Proyect Mano Gift
# menu de selección (opciones):
# # game (deshabilitada)
# # configuracion (deshabilitada)
# # debug screen
# # # seleccion de mapa.
# # # play.
class introduccion (Menu_Inventario):
    canvas = ''
    running = True
    sel = 0
    opciones = 0
    mapas = []
    def __init__ (self,ANCHO,ALTO):
        self.botones = sprite.LayeredDirty()
        self.botones.empty()
        self.canvas = self.crear_canvas(ANCHO,ALTO)
        self.crear_espacio_de_seleccion_de_mapas(ANCHO-17)
        self.crear_titulo("Mano-Gift:Debug Screen",self.font_high_color,self.bg_cnvs,ANCHO)
        botones = [{"boton":"Cargar","pos":[7,270],"derecha":"Salir"},
                   {"boton":"Salir","pos":[254,270],"izquierda":"Cargar"}]
        self.establecer_botones(botones)
    
    def cargar_mapas_iniciales(self):
        ok = []
        for mapa in os.listdir('maps'):
            ar = r.abrir_json('maps/'+mapa)
            if 'inicial' in ar['entradas']:
                ok.append(mapa.strip('.json'))
        
        return ok
    
    def crear_espacio_de_seleccion_de_mapas (self,ancho):
        mapas = self.crear_espacio_titulado(ancho,200,'Elija un mapa')
        rect = self.canvas.blit(mapas,(7,40))
        self.image = mapas.subsurface((0,0),(rect.w-8,rect.h-30))
        self.image.fill(self.bg_cnvs)
        fuente = font.SysFont('verdana', 16)
        self.mapas = self.cargar_mapas_iniciales() # lista
        self.opciones = len(self.mapas)
        texto = '\n'.join(self.mapas)
        render = render_textrect(texto,fuente,rect,self.font_high_color,self.bg_cnvs)
        self.image.blit(render,(3,0))
                
        return mapas
    
    def ejecutar (self,fondo):
        elegir_uno = False
        while self.running:
            T.FPS.tick(60)
            for event in EVENT.get():
                if event.type == QUIT:
                    py_quit()
                    sys.exit()
                    
                elif event.type == KEYDOWN:                 
                    if event.key == C.TECLAS.SALIR:
                        py_quit()
                        print('Saliendo...')
                        sys.exit()
                    
                    elif event.key == C.TECLAS.IZQUIERDA:
                        self.selectOne('izquierda')
                        
                    elif event.key == C.TECLAS.DERECHA:
                        self.selectOne('derecha')
                    
                    elif event.key == C.TECLAS.ARRIBA:
                        self.DeselectAllButtons()
                        self.sel = self.elegir_opcion(-1)
                        elegir_uno = True
                    
                    elif event.key == C.TECLAS.ABAJO:
                        self.DeselectAllButtons()
                        self.sel = self.elegir_opcion(+1)
                        elegir_uno = True
                    
                    elif event.key == C.TECLAS.HABLAR:
                        if self.current.nombre == "Cargar":
                            if elegir_uno:
                                self.PressOne()
                        else:
                            self.PressOne()
                        
                    
                elif event.type == KEYUP:
                    if event.key == C.TECLAS.HABLAR:
                        if self.current.nombre == "Cargar":
                            if elegir_uno:
                                self.running = False
                                W.cargar_hero()
                                W.setear_mapa(self.mapas[self.sel-1], 'inicial')
                            
                        elif self.current.nombre ==  "Salir":
                            py_quit()
                            print('Saliendo...')
                            sys.exit()
            
            self.canvas.blit(self.image,(10,66))
            fondo.blit(self.canvas,(10,10))
            pantalla.update()
