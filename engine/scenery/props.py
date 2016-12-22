from engine.globs.eventDispatcher import EventDispatcher
from engine.base import ShadowSprite, EventListener
from engine.globs import ItemGroup, ModData
from engine.globs.renderer import Renderer
from engine.misc import Resources
from pygame import mask, Rect
from .items import *


class Escenografia(ShadowSprite, EventListener):
    accion = None

    def __init__(self, nombre, x, y, z=0, data=None, imagen=None, rect=None):
        """
        :param nombre:
        :param imagen:
        :param x:
        :param y:
        :param data:
        :type nombre:str
        :type imagen:str
        :type x:int
        :type y:int
        :type data:dict
        :return:
        """
        self.nombre = nombre
        self.tipo = 'Prop'
        self.data = data
        if imagen is None and data is not None:
            imagen = data.get('image')
        super().__init__(imagen=imagen, rect=rect, x=x, y=y, dz=z)
        self.solido = 'solido' in data.get('propiedades', [])
        self.proyectaSombra = data.get('proyecta_sombra', True)
        self.descripcion = data.get('descripcion', "Esto es un ejemplo")
        self.face = data.get('cara', 'front')

        try:
            dialogo = Resources.abrir_json(ModData.dialogos + self.nombre + '.json')
            self.data.update({'dialog': dialogo})
        except IOError:
            pass

        self.add_listeners()  # carga de event listeners

    def rotate_view(self, np):
        pass

    def __repr__(self):
        return "<%s sprite(%s)>" % (self.__class__.__name__, self.nombre)


class Agarrable(Escenografia):
    def __init__(self, nombre, x, y, z, data):
        data.setdefault('proyecta_sombra', False)
        super().__init__(nombre, x, y, z, data)
        self.subtipo = data['subtipo']
        self.accion = 'agarrar'
        ItemGroup[self.nombre] = self

    def __call__(self):
        args = self.nombre, self.image, self.data
        if self.subtipo == 'consumible':
            return Consumible(*args)
        elif self.subtipo == 'equipable':
            return Equipable(*args)
        elif self.subtipo == 'armadura':
            return Armadura(*args)
        elif self.subtipo == 'arma':
            return Arma(*args)
        elif self.subtipo == 'accesorio':
            return Accesorio(*args)
        elif self.subtipo == 'pocion':
            return Pocion(*args)


class Movible(Escenografia):
    def __init__(self, nombre, x, y, z, data):
        p = data.get('propiedades', ['solido'])
        if 'solido' not in p:
            p.append('solido')
            data['propiedades'] = p
        super().__init__(nombre, x, y, z, data)
        self.accion = 'mover'
        ItemGroup[self.nombre] = self

    def mover(self, dx, dy):
        col_mapa = False
        if self.stage.mapa.mask.overlap(self.mask, (self.mapRect.x + dx, self.mapRect.y)) is not None:
            col_mapa = True

        if self.stage.mapa.mask.overlap(self.mask, (self.mapRect.x, self.mapRect.y + dy)) is not None:
            col_mapa = True

        if not col_mapa:
            self.reubicar(dx, dy)
            return True

        return False


class Trepable(Escenografia):
    def __init__(self, nombre, x, y, z, data):
        super().__init__(nombre, x, y, z, data)
        self.accion = 'trepar'


class Operable(Escenografia):
    estados = {}
    estado_actual = 0
    enabled = True

    def __init__(self, nombre, x, y, z, data):
        super().__init__(nombre, x, y, z, data)
        self.estados = {}
        self.accion = 'operar'
        self.enabled = self.data.get('enabled', True)
        ItemGroup[self.nombre] = self

        for estado in data['operable']:
            idx = estado['ID']
            self.estados[idx] = {}
            for attr in estado:
                if attr == 'image':
                    img = Resources.cargar_imagen(estado[attr])
                    mascara = mask.from_surface(img)
                    self.estados[idx].update({'image': img, 'mask': mascara})
                elif attr == 'next':
                    self.estados[idx].update({'next': estado[attr]})
                elif attr == 'event':
                    f = ModData.get_script_method(self.data['script'], estado[attr])
                    self.estados[idx].update({'event': f})
                else:
                    self.estados[idx].update({attr: estado[attr]})

    def operar(self, estado=None):
        if estado is None:
            self.estado_actual = self.estados[self.estado_actual]['next']
        else:
            self.estado_actual = estado
        for attr in self.estados[self.estado_actual]:
            if hasattr(self, attr):
                setattr(self, attr, self.estados[self.estado_actual][attr])
            elif attr == 'event':
                self.estados[self.estado_actual][attr](self.nombre, self.estados[self.estado_actual])


class Destruible(Escenografia):
    def __init__(self, nombre, x, y, z, data):
        super().__init__(nombre, x, y, z, data)
        self.accion = 'romper'


class Estructura3D(Escenografia):
    faces = {}
    face = 'front'
    _chopped = False

    def __init__(self, nombre, x, y, data):
        self.nombre = nombre
        self.faces = {'front': None, 'right': None, 'back': None, 'left': None}
        self.face = data.get('cara', 'front')
        self.x, self.y = x, y
        self.w, self.h = data['width'], data['height']
        self.rect = Rect(self.x, self.y, self.w, self.h)

        for face in data['componentes']:
            if len(data['componentes'][face]):
                self.faces[face] = self.build_face(data, x, y, face)

        self.props = self.faces[self.face]
        super().__init__(nombre, x, y, data=data, rect=self.rect)
        EventDispatcher.register(self.rotate_view, 'Rotar_Todo')

    def build_face(self, data, dx, dy, face):
        from engine.scenery import new_prop
        props = []
        for nombre in data['componentes'][face]:
            ruta = data['referencias'][nombre]
            imagen = None
            propdata = {}
            for x, y, z in data['componentes'][face][nombre]:
                if type(ruta) is dict:
                    propdata = ruta.copy()

                elif ruta.endswith('.json'):
                    propdata = Resources.abrir_json(ruta)

                elif ruta.endswith('.png'):
                    w, h = data['width'], data['height']
                    imagen = self.chop_faces(ruta, w=w, h=h)[face]

                if 'cara' not in propdata:
                    propdata.update({'cara': face})

                prop = new_prop(nombre, dx + x, dy + y, z=z, img=imagen, data=propdata)
                props.append(prop)

        return props

    def chop_faces(self, ruta_img, w, h):
        if not self._chopped:
            spritesheet = Resources.split_spritesheet(ruta_img, w=w, h=h)
            d = {}
            if len(spritesheet) > 1:
                for idx, face in [[0, "front"], [1, "left"], [2, "right"], [3, "back"]]:
                    d[face] = spritesheet[idx]
            else:
                d['front'] = spritesheet[0]
            self._chopped = d
            return d
        else:
            return self._chopped

    def rotate_view(self, event):
        np = event.data['view']
        objects_faces = ['front', 'right', 'back', 'left']
        idx = objects_faces.index(self.face)
        temp = [objects_faces[idx]] + objects_faces[idx + 1:] + objects_faces[:idx]

        for prop in self.faces[self.face]:
            Renderer.camara.remove_obj(prop)

        self.face = temp[np]

        for prop in self.faces[self.face]:
            Renderer.camara.add_real(prop)

