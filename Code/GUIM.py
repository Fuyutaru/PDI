# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:22:26 2024

@author: Laurie
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt

import Enumeration
import Champ





class GUIM(QDialog, QMainWindow):
    def __init__(self, champs):
        super(GUIM, self).__init__()
        self.champs = champs
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        
        #TEST D'AJOUT DES CHAMPS
        self.bouton = QPushButton("Ajouter champs")
        self.bouton.clicked.connect(self.ajouterChamps)
        self.mainLayout.addWidget(self.boutonAjouter, alignment=Qt.AlignLeft)
        
        # Ajout tableau pour afficher les données
        self.tableau = QTableWidget()
        self.mainLayout.addWidget(self.tableau)
        self.mainLayout.addWidget(self.boutonCharger, alignment=Qt.AlignLeft)
        
        #Bouton pour ajouter donnée
        self.boutonCharger = QPushButton("Charger Données")
        self.boutonCharger.clicked.connect(self.chargerDonnees)
        self.mainLayout.addWidget(self.boutonCharger)
        
        self.setLayout(self.mainLayout)
        
    
    def chargerDonnees(self):
        # Ouvrir une boîte de dialogue pour sélectionner le fichier
        filename, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Fichiers XML (*.xml);;Tous les fichiers (*.*)")
        
        if filename:
            try:
                with open(filename, 'r') as file:
                    donnees = file.read()
                    self.afficherDonneesDansTableau(donnees)
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier : {str(e)}")

    def afficherDonneesDansTableau(self, donnees):
        self.tableau.clear()
        
        # Déterminer le nombre de lignes nécessaires pour afficher les données
        lines = donnees.split('\n')
        num_rows = len(lines)
        
        # Définir le nombre de colonnes
        num_columns = len(lines[0].split(',')) if lines else 0
        
        # Redimensionner le tableau en fonction du nombre de lignes et de colonnes
        self.tableau.setRowCount(num_rows)
        self.tableau.setColumnCount(num_columns)
        
        # Remplir le tableau avec les données
        for i, line in enumerate(lines):
            items = line.split(',')
            for j, item in enumerate(items):
                self.tableau.setItem(i, j, QTableWidgetItem(item.strip()))
                
                
    
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
        
    
    def save():
        pass
    
    


