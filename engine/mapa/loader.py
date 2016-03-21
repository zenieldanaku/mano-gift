from engine.globs import EngineData as Ed, Constants as Cs, MobGroup, ItemGroup, ModData as Md
from engine.misc import Resources as Rs
from engine.mobs import PC, NPC
from engine.scenery import new_prop
from .salida import Salida


class Loader:
    STAGE = None

    @classmethod
    def set_stage(cls, stage):
        cls.STAGE = stage

    @classmethod
    def load_everything(cls, entrada, mobs_data):
        cls.cargar_hero(entrada)
        cls.cargar_props()
        cls.cargar_mobs(mobs_data)
        cls.cargar_salidas()

    @classmethod
    def cargar_props(cls, ):
        imgs = cls.STAGE.data['refs']
        """:type imgs: dict"""
        pos = cls.STAGE.data['capa_ground']['props']

        for ref in pos:
            try:
                data = Rs.abrir_json(Md.items + ref + '.json')
                if ref in imgs:
                    imagen = Rs.cargar_imagen(imgs[ref])
                else:
                    imagen = Rs.cargar_imagen(data['image'])
            except IOError:
                data = False
                imagen = Rs.cargar_imagen(imgs[ref])

            for x, y in pos[ref]:
                if data:
                    prop = new_prop(ref, imagen, x, y, data)
                    is_interactive = True
                    ItemGroup[ref] = prop
                else:
                    prop = new_prop(ref, imagen, x, y)
                    is_interactive = False

                cls.STAGE.add_property(prop, Cs.GRUPO_ITEMS, is_interactive)

    @classmethod
    def cargar_mobs(cls, extra_data, capa='capa_ground'):
        for key in cls.STAGE.data[capa]['mobs']:
            pos = cls.STAGE.data[capa]['mobs'][key]
            if key == 'npcs':
                clase = NPC

                for ref in pos:
                    data = Rs.abrir_json(Md.mobs + ref + '.json')
                    data.update(extra_data[ref])
                    for x, y in pos[ref]:
                        mob = clase(ref, x, y, data)
                        if capa == 'capa_ground':
                            cls.STAGE.add_property(mob, Cs.GRUPO_MOBS)

    @classmethod
    def cargar_hero(cls, entrada):
        x, y = cls.STAGE.data['entradas'][entrada]
        try:
            pc = MobGroup['heroe']
            Ed.HERO = pc
            Ed.HERO.ubicar(320, 240)
            Ed.HERO.mapX = x
            Ed.HERO.mapY = y
            print(Ed.HERO.z)
            # Ed.HERO.z = y + 53

        except (IndexError, KeyError, AttributeError):
            Ed.HERO = PC(Rs.abrir_json(Md.mobs + 'hero.json'), x, y)

        if Ed.HERO not in cls.STAGE.properties:
            Loader.STAGE.add_property(Ed.HERO, Cs.GRUPO_MOBS)

    @classmethod
    def cargar_salidas(cls):
        salidas = cls.STAGE.data['salidas']
        for salida in salidas:
            sld = Salida(salida, salidas[salida])
            cls.STAGE.add_property(sld, Cs.GRUPO_SALIDAS)
