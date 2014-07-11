#from engine.misc import Resources as r
from .renderer import Renderer
#from .mod_data import ModData as MD

class EngineData:    
    mapas = {}
    MAPA_ACTUAL = ''
    HERO = ''
    menu_actual = ''
    menu_previo = ''
    MENUS = {}
    DIALOG = None
    MODO = ''
    onPause = False
    RENDERER = Renderer()
    HUD = None
    
    def setear_mapa(mapa, entrada):
        ED = EngineData
        ED.MODO = 'Aventura'
        from engine.mapa import Stage
        if mapa not in ED.mapas:
            ED.mapas[mapa] = Stage(mapa,entrada)
        ED.MAPA_ACTUAL = ED.mapas[mapa]
        ED.RENDERER.setBackground(ED.MAPA_ACTUAL.mapa)
        for obj in ED.MAPA_ACTUAL.properties:
            ED.RENDERER.addObj(obj,obj.rect.bottom)
        ED.RENDERER.camara.centrar()