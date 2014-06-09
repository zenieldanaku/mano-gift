from engine.misc import Resources as r
from .renderer import Renderer

class EngineData:    
    mapas = {}
    MAPA_ACTUAL = ''
    HERO = ''
    menu_actual = ''
    menu_previo = ''
    MENUS = {}
    DIALOG = None
    MODO = 'Aventura'
    onPause = False
    RENDERER = Renderer()
    mod_folder = ''
    
    def setear_mapa(mapa, entrada):
        ED = EngineData
        from engine.mapa import Stage
        if mapa not in ED.mapas:
            ED.mapas[mapa] = Stage(r.abrir_json('data/maps/'+mapa+'.json'),entrada)
        ED.MAPA_ACTUAL = ED.mapas[mapa]
        ED.RENDERER.setBackground(ED.MAPA_ACTUAL.mapa)
        for obj in ED.MAPA_ACTUAL.properties:
            ED.RENDERER.addObj(obj,obj.rect.bottom)
        ED.RENDERER.camara.centrar()