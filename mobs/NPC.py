from . import Mob
from .MobGroup import MobGroup
from globs import World as W, QuestManager

class NPC (Mob):
    quest = None
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.data = data
        self.nombre = nombre
        self.dialogos = self.data['dialogo']
        self.pos_diag = -1
        MobGroup.addMob(self)
        if 'quest' in data:
            QuestManager.add(data['quest'])
    
    def hablar(self, opcion=1):
        if len(self.dialogos) == 0:
            return False
        
        elif not W.onSelect:
            self.pos_diag += 1
        
        if self.pos_diag >= len(self.dialogos):
            self.stage.endDialog()
            self.pos_diag = -1
            return False
        
        else:
            if type(self.dialogos[self.pos_diag]) != dict:
                texto = self.dialogos[self.pos_diag]
                W.onSelect = False
            
            else:
                if not W.onSelect:
                    texto = '\n'.join(self.dialogos[self.pos_diag])
                    W.onSelect = True
                    
                else:
                    sel = list(self.dialogos[self.pos_diag].keys())[opcion-1]
                    texto = self.dialogos[self.pos_diag][sel]
                    W.onSelect = False
                
            self.stage.setDialog(texto)
            return True
    
    def devolver_seleccion(self,sel):
        op = list(self.dialogos[self.pos_diag].keys())[W.DIALOG.sel-1]
        
        return self.dialogos[self.pos_diag][op]
        
    def mover(self):
        if self.pos_diag == -1:
            super().mover()