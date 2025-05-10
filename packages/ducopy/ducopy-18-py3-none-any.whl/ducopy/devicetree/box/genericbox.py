from ducopy.devicetree.box.abstractbox import AbstractBox

class GenericBox(AbstractBox):
    def __init__(self, name):
        self._name = name

    def name(self) -> str:
        return f'GenericBoxAdapter {self._name}'