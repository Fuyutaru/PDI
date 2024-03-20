

class Champ():
    def __init__(self, nom, type, balise):
        self.nom = nom
        self.type = type
        self.balise = balise
        self.valeur = None
    
    @property
    def valeur(self):
        return self.valeur
    
    # on peut juste faire champ_instance.valeur = "example_value"

    @valeur.setter
    def valeur(self, new_value):
        self.valeur = new_value
    