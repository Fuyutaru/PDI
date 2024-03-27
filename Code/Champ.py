class Champ():
    def __init__(self, nom, type, balise):
        self.nom = nom
        self.type = type
        self.balise = balise
        self._valeur = None
    
    @property
    def valeur(self):
        return self._valeur
    
    @valeur.setter
    def valeur(self, new_value):
        if new_value != self._valeur:
            self._valeur = new_value
