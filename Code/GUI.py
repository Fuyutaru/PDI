# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:03:51 2024

@author: Svetie
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt


import Champ

class GUI(QDialog, QMainWindow):
    def __init__(self, champs):
        super(GUI, self).__init__()
        self.champs = champs
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        
        #TEST D'AJOUT DES CHAMPS
        self.bouton = QPushButton("Ajouter champs")
        self.bouton.clicked.connect(self.ajouterChamps)
        self.mainLayout.addWidget(self.bouton)
        self.setLayout(self.mainLayout)
        
    def save():
        pass
    
    def ajouterChamps(self):
        for champ in self.champs :
            champLayout = QHBoxLayout()
            nom = QLabel(champ.nom)
            champLayout.addWidget(nom)
            champLayout.addWidget(QLineEdit())
            typeChamp = QLabel("(" + champ.type + ")")
            champLayout.addWidget(typeChamp)
            self.mainLayout.addLayout(champLayout)
            
            self.setLayout(self.mainLayout)
        pass
    
    def ajouterTab():
        pass