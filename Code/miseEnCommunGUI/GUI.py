# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:06:36 2024

@author: Svetie
"""

import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem

import data_handling as dh
import FileLoader
import Enumeration
from Champ import Champ

class GUI(QDialog, QMainWindow):
    def __init__(self, champs):
        super(GUI, self).__init__()
        self.champs = champs
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        
        self.specification_xml_path = None
        self.data_xml_path = None
        self.specification_xml_structure = None
        
        # #TEST D'AJOUT DES CHAMPS
        # self.bouton = QPushButton("Ajouter champs")
        # self.bouton.clicked.connect(self.ajouterChamps)
        # self.mainLayout.addWidget(self.bouton)
        
        # self.setWindowTitle('Éditeur de Fichiers XML')
        # self.setGeometry(100, 100, 800, 600)
        # self.setWindowIcon(QIcon('./icone.png'))

        # # Barre de menu
        # menuBar = self.menuBar()
        # menuBar.setStyleSheet("QMenuBar { background-color: #e1e1e1; color: #333333; }")
        # fileMenu = menuBar.addMenu('&Fichier')

        # # Actions du menu
        # loadSpecAction = QAction(QIcon('./icone.png'), 'Charger Spécification', self)
        # loadSpecAction.triggered.connect(self.loadSpecificationXml)
        # fileMenu.addAction(loadSpecAction)

        # loadDataAction = QAction(QIcon('./icone.png'), 'Charger Données XML', self)
        # loadDataAction.triggered.connect(self.loadDataXml)
        # fileMenu.addAction(loadDataAction)

        # # # Text Editor
        # # self.textEdit = QTextEdit(self)
        # # self.textEdit.setStyleSheet("QTextEdit {border: 1px solid black; background-color: #f0f0f0;}")

        # # Buttons
        # saveButton = QPushButton(QIcon('./icon.png'), 'Sauvegarder', self)
        # saveButton.clicked.connect(self.saveDataXml)
        # saveButton.setToolTip('Sauvegarder le fichier XML')

        # # Layouts
        # self.mainLayout = QVBoxLayout()
        # # self.mainLayout.addWidget(self.textEdit)
        
        # buttonsLayout = QHBoxLayout()
        # buttonsLayout.addWidget(saveButton)
        # self.mainLayout.addLayout(buttonsLayout)

        # centralWidget = QWidget()
        # centralWidget.setLayout(self.mainLayout)
        # self.setCentralWidget(centralWidget)

        # # Status Bar
        # self.statusBar = QStatusBar()
        # self.setStatusBar(self.statusBar)
        
        # self.setLayout(self.mainLayout)

            #TEST D'AJOUT DES CHAMPS
        
        self.champs = champs
        
    

    def initUI(self):
        self.setWindowTitle('Éditeur de Fichiers XML')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('./icone.png'))

        # Barre de menu
        menuBar = self.menuBar()
        menuBar.setStyleSheet("QMenuBar { background-color: #e1e1e1; color: #333333; }")
        fileMenu = menuBar.addMenu('&Fichier')

        # Actions du menu
        loadSpecAction = QAction(QIcon('./icone.png'), 'Charger Spécification', self)
        loadSpecAction.triggered.connect(self.loadSpecificationXml)
        fileMenu.addAction(loadSpecAction)

        loadDataAction = QAction(QIcon('./icone.png'), 'Charger Données XML', self)
        loadDataAction.triggered.connect(self.loadDataXml)
        fileMenu.addAction(loadDataAction)

        # # Text Editor
        # self.textEdit = QTextEdit(self)
        # self.textEdit.setStyleSheet("QTextEdit {border: 1px solid black; background-color: #f0f0f0;}")

        # Buttons
        saveButton = QPushButton(QIcon('./icon.png'), 'Sauvegarder', self)
        saveButton.clicked.connect(self.saveDataXml)
        saveButton.setToolTip('Sauvegarder le fichier XML')

        # Layouts
        self.mainLayout = QVBoxLayout()
        # self.mainLayout.addWidget(self.textEdit)
        
        ####TEST CHAMPS####
        self.bouton = QPushButton("Ajouter champs")
        self.bouton.clicked.connect(self.ajouterChamps)
        self.mainLayout.addWidget(self.bouton)
        ####TEST CHAMPS####

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(saveButton)
        self.mainLayout.addLayout(buttonsLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        

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

    def loadSpecificationXml(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de spécification XML', '', 'XML files (*.xml)')
        if path:
            self.specification_xml_path = path
            tree = ET.parse(self.specification_xml_path)
            self.specification_xml_structure = dh.analyzeSpecification(tree)
            QMessageBox.information(self, 'Succès', 'Fichier de spécification chargé avec succès!')
        else:
            QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de spécification.')

    def loadDataXml(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de données XML', '', 'XML files (*.xml)')
        if path:
            self.data_xml_path = path
            self.loader = FileLoader(path)
            self.loader.fileLoaded.connect(self.onFileLoaded)
            self.loader.start()

    def onFileLoaded(self, data):
        self.textEdit.setText(data)
        QMessageBox.information(self, 'Succès', 'Fichier de données XML chargé avec succès!')

    def saveDataXml(self):
        if dh.validateXml(self.textEdit.toPlainText(), self.specification_xml_structure):
            if not self.data_xml_path:
                path, _ = QFileDialog.getSaveFileName(self, 'Enregistrer le fichier de données XML', '', 'XML files (*.xml)')
                if path:
                    self.data_xml_path = path
            with open(self.data_xml_path, 'w') as file:
                file.write(self.textEdit.toPlainText())
            QMessageBox.information(self, 'Succès', 'Fichier de données XML enregistré avec succès!')
        else:
            QMessageBox.warning(self, 'Erreur', 'Le fichier de données XML contient des erreurs.')


if __name__ == "__main__":
    
    champ1 = Champ("Number", "int", 1)
    champ2 = Champ("Id", "int", 2)
    champ3 = Champ("Name", "string", 3)
    champ4 = Champ("Number", "int", "el")
    champ5 = Champ("Id", "int", "el")
    champ6 = Champ("Name", "string", "el")
    champ7 = Champ("Systeme de coordonnées", "enum_SysCoGeo", 4)
    champs= [champ1, champ2, champ4, champ5, champ6, champ3, champ7, champ4, champ5]
    
    app = QApplication(sys.argv)
    gui = GUI(champs)
    gui.show()
    sys.exit(app.exec_())
