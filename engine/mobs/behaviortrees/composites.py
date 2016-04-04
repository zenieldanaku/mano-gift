from .status import *
from .node import Node

__all__ = ['Composite', 'Secuence', 'Selector', 'Parallel']


class Composite(Node):
    type = 'Composite'
    children = None
    current_id = None

    def __init__(self, tree, idx, children):
        # these are NOT containers, they just point to their children
        super().__init__(tree, idx)
        self.children = [child for child in children]
        self.current_id = 0

    def update(self):
        child = self.children[self.current_id]
        child.update()

    def reset(self):
        self.current_id = -1


class Secuence(Composite):
    name = 'Secuence'

    def __repr__(self):
        lista = [str(c.idx) for c in self.children]
        return ' '.join([self.type, '#' + str(self.idx), self.name, '(' + ', '.join(lista) + ')'])

    def get_child_status(self, status):
        if status is Success:
            if not self.current_id + 1 == len(self.children):
                self.current_id += 1
                status = Running

        if status is Running:
            self.tree.set_to_check(self.children[self.current_id])

        if self.parent is not None:
            self.parent.get_child_status(status)

        elif status is Success:
            self.tree.reset()

class Selector(Composite):
    name = 'Selector'

    def __repr__(self):
        lista = [str(c.idx) for c in self.children]
        return ' '.join([self.type, '#' + str(self.idx), self.name, '(' + ', '.join(lista) + ')'])

    def get_child_status(self, status):
        if status is Failure:
            if not self.current_id + 1 == len(self.children):
                self.current_id += 1
                status = Running

        if status is Running:
            self.tree.set_to_check(self.children[self.current_id])

        if self.parent is not None:
            self.parent.get_child_status(status)

        elif status is Success:
            self.tree.reset()


class Parallel(Composite):
    # based on http://guineashots.com/2014/08/10/an-introduction-to-behavior-trees-part-2/

    name = 'Parallel'
    children_status = []
    success_value = 0
    failure_value = 0

    def __init__(self, tree, idx, children, s=0, f=0):
        super().__init__(tree, idx, children)
        self.children_status = [i*0 for i in children]
        self.success_value = s
        self.failure_value = f

    def __repr__(self):
        lista = [str(c.idx) for c in self.children]
        return ' '.join([self.type, '#' + str(self.idx), self.name, '(' + ', '.join(lista) + ')'])

    def update(self):
        for child in self.children:
            child.update()
        self.reset()

    def get_child_status(self, status):
        self.children_status[self.current_id] = status
        self.current_id += 1
        if self.children_status.count(Success) >= self.success_value:
            self.parent.get_child_status(Success)

        elif self.children_status.count(Failure) >= self.failure_value:
            self.parent.get_child_status(Failure)

        else:
            self.parent.get_child_status(Running)
