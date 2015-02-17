class Equipado:
    equipo = {'yelmo': None, 'aro 1': None, 'aro 2': None, 'cuello': None, 'peto': None,
              'guardabrazos': None, 'brazales': None, 'faldar': None, 'quijotes': None,
              'grebas': None, 'mano buena': None, 'mano mala': None, 'botas': None, 'capa': None,
              'cinto': None, 'guantes': None, 'anillo 1': None, 'anillo 2': None}
    inventario = None

    def equipar_item(self, item):
        self.equipo[item.espacio] = item
        self.inventario.remover(item)

    def desequipar_item(self, item):
        self.equipo[item.espacio] = None
        self.inventario.agregar(item)