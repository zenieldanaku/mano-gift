from engine.mobs.behaviortrees import BehaviourTree
from engine.globs import EngineData, ModData
from engine.misc.resources import abrir_json
from engine.mobs import ControllableAI
from . import Sensitivo, Animado


class Autonomo(Sensitivo, Animado):  # tiene que poder ver para ser autónomo
    AI = None  # determina cómo se va a mover el mob
    _AI = None  # copia de la AI original
    AI_type = ''  # 'Controllable' or  'Autonomous'

    def __init__(self, data, **kwargs):
        ai_name = data['AI']

        self.AI = self.create_ai(ai_name)
        self._AI = self.AI
        super().__init__(data, **kwargs)

    def create_ai(self, name):
        if name == 'controllable':
            self.AI_type = 'Controllable'
            return ControllableAI(self)

        else:
            self.AI_type = 'Autonomous'
            tree_data = abrir_json(ModData.mobs + 'behaviours/' + name + '.json')
            return BehaviourTree(self, tree_data)

    def update(self, *args):
        super().update(*args)
        if not EngineData.onPause:
            self.AI.update()
