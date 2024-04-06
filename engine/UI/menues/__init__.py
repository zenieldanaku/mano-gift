from .pausa import MenuPausa
from .equipo import MenuEquipo
from .opciones import MenuOpciones
from .cargar import MenuCargar
from .principal import MenuPrincipal
from .menu import Menu
from .model import MenuModel
from .name import MenuName
from .ability import MenuAbility
from .compraventa import MenuBuy, MenuSell

default_menus = {'MenuPausa': MenuPausa,
                 'MenuEquipo': MenuEquipo,
                 'MenuCargar': MenuCargar,
                 'MenuPrincipal': MenuPrincipal,
                 'MenuOpciones': MenuOpciones,
                 'MenuNuevo': MenuModel,  # en realidad sería MenuModel,
                 'MenuName': MenuName,  # pero está así para que diga "nuevo" en Principal.
                 'MenuAbility': MenuAbility  # No es el verdadero (y viejo) "MenuNuevo".
                 }

# estructuras para los menues raiz Principal y Pausa.
# No son lo más "automático" que se puede hacer,
# pero son lo más aproximado y menos explicito que se me ocurre.

# Botones del Menú Pausa
pause_menus = [
    'MenuEquipo',
    'MenuOpciones',
    'MenuCargar'
]

# Botones del Menú Principal
inital_menus = [
    'MenuNuevo',
    'MenuCargar',
    'MenuOpciones',
]

# Menúes de compraventa (issue #53)
trading_menus = {
    "MenuComprar": MenuBuy,
    "MenuVender": MenuSell
}

__all__ = [
    'Menu',
    "default_menus",
    'pause_menus',
    'inital_menus',
    "trading_menus"
]
