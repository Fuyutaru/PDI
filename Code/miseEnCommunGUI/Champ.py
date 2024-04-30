<<<<<<<< HEAD:Code/Field.py
class Field():
    def __init__(self, name, type, path, value):
        self.name = name
        self.type = type
        self.path = path
        self._value = value
========
class Champ():
    def __init__(self, nom, type, path):
        self.nom = nom
        self.type = type
        self.path = path
        self._valeur = None
>>>>>>>> Tableau:Code/miseEnCommunGUI/Champ.py
    
    @property
    def valeur(self):
        return self._valeur
    
    @valeur.setter
    def valeur(self, new_value):
        if new_value != self._valeur:
            self._valeur = new_value
