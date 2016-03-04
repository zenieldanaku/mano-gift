from engine.globs.renderer import Renderer

class damageableSprite: #(AzoeSprite):
    salud = 0
    
    def recibir_danio(self):
        from engine.globs import MobGroup
        self.salud -= 1
       
        if self.salud <= 0:
            if self.death_img is not None:
                self.image = self.death_img
            else: # esto queda hasta que haga sprites 'muertos' de los npcs
                Renderer.delObj(self)
                self.stage.del_property(self)
            self.dead = True
            MobGroup.remove(self)

