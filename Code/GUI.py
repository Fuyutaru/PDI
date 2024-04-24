# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:03:51 2024

"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt

import Enumeration
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
        listeChampTableau = []
        n = len(self.champs)
        for i in range(n):
            if self.champs[i].balise == "el" :
                if i == n-1 or (i < n-1 and self.champs[i+1].balise != "el"):
                    listeChampTableau.append(self.champs[i])
                    self.ajouterTab(listeChampTableau)
                    listeChampTableau = []
                else :
                    listeChampTableau.append(self.champs[i])
            elif self.champs[i].type in Enumeration.enumDict :
                enumComboBox = QComboBox()
                enumComboBox.addItems(Enumeration.enumDict[self.champs[i].type])
                
                enumLayout = QHBoxLayout()
                nom = QLabel(self.champs[i].nom)
                enumLayout.addWidget(nom)
                enumLayout.addWidget(enumComboBox)
                typeEnum = QLabel("(" + self.champs[i].type + ")")
                enumLayout.addWidget(typeEnum)
                self.mainLayout.addLayout(enumLayout)
            else :
                champLayout = QHBoxLayout()
                nom = QLabel(self.champs[i].nom)
                champLayout.addWidget(nom)
                champLayout.addWidget(QLineEdit())
                typeChamp = QLabel("(" + self.champs[i].type + ")")
                champLayout.addWidget(typeChamp)
                self.mainLayout.addLayout(champLayout)
                
        self.setLayout(self.mainLayout)
        
        
    
    def ajouterTab(self, listeChampTableau):
        
            
        def addLine():
            rowPosition = tableau.rowCount()
            tableau.insertRow(rowPosition)
            
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)

        
        tableau = QTableWidget()
        
        n = len(listeChampTableau)
        tableau.setRowCount(1)
        tableau.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append(listeChampTableau[i].nom)
        tableau.setHorizontalHeaderLabels(columns)
        
        tableau.move(0, 0)
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(tableau)
        tabLayout.addWidget(addButton)
        self.mainLayout.addLayout(tabLayout)




