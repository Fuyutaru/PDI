class Field():
    def __init__(self, name, type, root, value):
        self.name = name
        self.type = type
        self.root = root
        self._value = value
    
    @property
    def valeur(self):
        return self._valeur
    
    @valeur.setter
    def valeur(self, new_value):
        if new_value != self._valeur:
            self._valeur = new_value
