# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 16:36:50 2024

@author: Svetie
"""

class Champ():
    def __init__(self, nom, type, balise, boxLayout):
        self.nom = nom
        self.type = type
        self.balise = balise
        self._valeur = None
        self.boxLayout = boxLayout
    
    @property
    def valeur(self):
        return self._valeur
    
    @valeur.setter
    def valeur(self, new_value):
        if new_value != self._valeur:
            self._valeur = new_value
