from pygame import event as EVENT, quit as py_quit
from pygame import QUIT, KEYUP, KEYDOWN
from globs import Constants as C, World as W
import sys

class modo:
    dx,dy = 0,0
    onSelect = False
    newMenu = False
    onVSel = False
    def Juego (events):
        for event in events:
            if event.type == QUIT:
                py_quit()
                sys.exit()
            
            elif event.type == KEYDOWN:
                if event.key == C.TECLAS.SALIR:
                    py_quit()
                    print('Saliendo...')
                    sys.exit()
                
                elif event.key == C.TECLAS.DEBUG:
                    print((W.HERO.mapX, W.HERO.mapY))
    
    def Aventura(events,fondo):
        dx, dy = modo.dx, modo.dy
        for event in events:
            if event.type == KEYDOWN:
                if event.key == C.TECLAS.IZQUIERDA: dx += 1
                elif event.key == C.TECLAS.DERECHA: dx -= 1
                elif event.key == C.TECLAS.ARRIBA:  dy += 1
                elif event.key == C.TECLAS.ABAJO:   dy -= 1
                    
                elif event.key == C.TECLAS.HABLAR:
                    W.MODO = 'Dialogo'
                    modo.onSelect = W.HERO.hablar(modo.onSelect)
                    
                elif event.key == C.TECLAS.INVENTARIO:
                    W.MODO = 'Dialogo'
                    modo.onVSel = True
                    W.HERO.ver_inventario()
                
                elif event.key == C.TECLAS.POSICION_COMBATE:
                    W.HERO.cambiar_estado()
                
                elif event.key == C.TECLAS.ACCION:
                    W.HERO.accion()
                
                elif event.key == C.TECLAS.MENU:
                    W.onPause = True
                    W.MODO = 'Menu'
                    modo.onVSel = W.MAPA_ACTUAL.popMenu('Pausa')
                    
            elif event.type == KEYUP:
                if event.key == C.TECLAS.IZQUIERDA or event.key == C.TECLAS.DERECHA:
                    dx = 0
                elif event.key == C.TECLAS.ABAJO or event.key == C.TECLAS.ARRIBA:
                    dy = 0
        
        if dx != 0 or dy != 0:
            W.HERO.mover(-dx,-dy)
            W.MAPA_ACTUAL.mover(dx,dy)
        modo.dx, modo.dy = dx, dy
        
        return W.MAPA_ACTUAL.update(fondo)
    
    def Dialogo(events,fondo):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == C.TECLAS.ARRIBA: W.DIALOG.elegir_opcion(-1)
                elif event.key == C.TECLAS.ABAJO: W.DIALOG.elegir_opcion(+1)
                
                elif event.key == C.TECLAS.HABLAR:
                    if modo.onSelect:
                        modo.onSelect = W.HERO.confirmar_seleccion()
                    elif modo.onVSel:
                        W.DIALOG.confirmar_seleccion()
                    else:
                        modo.onSelect = W.HERO.hablar(modo.onSelect)
                
                elif event.key == C.TECLAS.INVENTARIO:
                    W.MAPA_ACTUAL.endDialog()
                    W.MODO = 'Aventura'
                    modo.onVSel = False
                
                elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                    W.MAPA_ACTUAL.endDialog()
                    pass # cancelaria el dialogo como lo hace ahora.
        
        return W.MAPA_ACTUAL.update(fondo)
    
    def Menu(events,fondo):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == C.TECLAS.IZQUIERDA:
                    W.menu_actual.usar_funcion('izquierda')
                
                elif event.key == C.TECLAS.DERECHA:
                    W.menu_actual.usar_funcion('derecha')
                
                elif event.key == C.TECLAS.ARRIBA:
                    W.menu_actual.usar_funcion('arriba')
                        
                elif event.key == C.TECLAS.ABAJO:
                    W.menu_actual.usar_funcion('abajo')
                
                elif event.key == C.TECLAS.HABLAR:
                    modo.newMenu = W.menu_actual.usar_funcion('hablar')
                
                elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                    'Retrocede al menú anterior, o sale del modo'
                    if W.menu_actual.nombre == 'Pausa':
                        W.MAPA_ACTUAL.endDialog()
                        W.onPause = False
                    else:
                        W.MAPA_ACTUAL.popMenu(W.menu_previo)
            
            elif event.type == KEYUP:
                if event.key == C.TECLAS.HABLAR:
                    if modo.newMenu:
                        W.MAPA_ACTUAL.popMenu(W.menu_actual.current.nombre)
                
        return W.MAPA_ACTUAL.update(fondo)