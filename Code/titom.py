# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 16:43:48 2024

@author: Laurie
"""

from PyQt5.QtWidgets import QApplication
import sys
from GUIM import GUIM

def test():
    app = QApplication(sys.argv)
    
    # Création d'une instance de GUIM
    guim = GUIM(None)  
    
    # Charger les données à partir d'un fichier XML
    guim.chargerDonnees()
    
    # Afficher les données dans le tableau
    guim.afficherDonneesDansTableau()
    
    # Afficher la fenêtre
    guim.exec_()

if __name__ == "__main__":
    test()



"""
ajout d'ajouter un fichier de donnée'
recup nom tableau  type, donnée entré dans le tableau, nom colonne sur premiere ligne

Nom_tab([(Nom_colonne1,type) ( NomColonne2,type)...][coloneeligne1...], el)

pour presenter le tableau dans le dico

voir comment avec les données du fichier de donnée les mettre dans le champs

"""