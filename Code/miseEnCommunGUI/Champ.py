class Champ():
    def __init__(self, nom, type, path):
        self.nom = nom
        self.type = type
        self.path = path
        self._valeur = None
    
    @property
    def valeur(self):
        return self._valeur
    
    @valeur.setter
    def valeur(self, new_value):
        if new_value != self._valeur:
            self._valeur = new_value
