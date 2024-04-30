# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:57:27 2024

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

class XmlEditorGUI(QMainWindow):
    def __init__(self, champs): #Champs sera a retirer quand on aura la conversion
                                #des fichiers XML en liste de champs
        super().__init__()
        self.specification_xml_path = None
        self.data_xml_path = None
        self.specification_xml_structure = None
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        
        self.countTable = 0
        
        #TEST D'AJOUT DES CHAMPS
        
        self.champs = champs
        
    

    
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
        #saveButton.clicked.connect(self.saveDataXml)
        saveButton.clicked.connect(self.extraireDonneesEtTypes)
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
    
    def ajouterChamps(self):
        listChampTable = []
        n = len(self.champs)
        for i in range(n):
            typeChamp = self.champs[i].type
            pathChamp = self.champs[i].path
            pathChampSplit = self.champs[i].path.split("/")
            pathChampSplitNext = []
            
            
            if i < n-1 :
                pathChampSplitNext = self.champs[i+1].path.split("/")
            
            if pathChampSplit[-1] == "el" :
                self.addTable(pathChampSplit[-2], pathChamp, typeChamp)            
                        
            elif pathChampSplit[-2] == "el" :
                if i == n-1 or (pathChampSplit[:-1] != pathChampSplitNext[:-1]) :
                    listChampTable.append([pathChampSplit[-1], typeChamp[0]])
                    name = pathChampSplit[-3]
                    path = pathChamp[:-len(pathChampSplit[-1])]
                    self.addChampTable(listChampTable, path, name)
                    listChampTable = []
                    
                else :
                    listChampTable.append([pathChampSplit[-1], typeChamp[0]])
            
            elif len(typeChamp) != 1 :
                name = QLabel(pathChampSplit[-1])
                multiTypeLayout = QHBoxLayout()
                multiTypeLayout.addWidget(name)
                count = 1
                for t in typeChamp :
                    if t in Enumeration.enumDict :
                        enumComboBox = QComboBox()
                        enumComboBox.addItems(Enumeration.enumDict[t])
                        enumComboBox.setObjectName(pathChamp + "/" + str(count) + " " + t)
                        enumLayout = QHBoxLayout()
                        enumLayout.addWidget(enumComboBox)
                        typeEnum = QLabel("(" + t + ")")
                        enumLayout.addWidget(typeEnum)
                        multiTypeLayout.addLayout(enumLayout)
                        count+=1
                    else :
                        champLayout = QHBoxLayout()
                        champ = QLineEdit()
                        champ.setObjectName(pathChamp + "/" + str(count) + " " + t)
                        champLayout.addWidget(champ)
                        typeChamp = QLabel("(" + t + ")")
                        champLayout.addWidget(typeChamp)
                        count+=1
                        multiTypeLayout.addLayout(champLayout)
                        
                self.mainLayout.addLayout(multiTypeLayout)
                
                        
                        
            
            elif typeChamp[0] in Enumeration.enumDict :
                enumComboBox = QComboBox()
                enumComboBox.addItems(Enumeration.enumDict[typeChamp[0]])
                enumComboBox.setObjectName(pathChamp + " " + typeChamp[0])
                enumLayout = QHBoxLayout()
                nom = QLabel(pathChampSplit[-1])
                enumLayout.addWidget(nom)
                enumLayout.addWidget(enumComboBox)
                typeEnum = QLabel("(" + typeChamp[0] + ")")
                enumLayout.addWidget(typeEnum)
                self.mainLayout.addLayout(enumLayout)
            
            
            else :
                champLayout = QHBoxLayout()
                nom = QLabel(pathChampSplit[-1])
                champ = QLineEdit()
                champ.setObjectName(pathChamp + " " + typeChamp[0])
                champLayout.addWidget(nom)
                champLayout.addWidget(champ)
                typeChamp = QLabel("(" + typeChamp[0] + ")")
                champLayout.addWidget(typeChamp)
                self.mainLayout.addLayout(champLayout)
                
        self.setLayout(self.mainLayout)
    
    def addTable(self, name, path, types):
        
        def addLine():
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)
        
        
        tableName = QLabel(name)
        
        table = QTableWidget()
        table.setObjectName(path + " el")
        
        n = len(types)
        table.setRowCount(1)
        table.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append("(" + types[i] + ")")
        table.setHorizontalHeaderLabels(columns)
        
        table.move(0, 0)
        
        completeLayout = QVBoxLayout()
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(table)
        tabLayout.addWidget(addButton)
        
        completeLayout.addWidget(tableName)
        completeLayout.addLayout(tabLayout)
        self.mainLayout.addLayout(completeLayout)
        
        
    
    def addChampTable(self, listChampTable, path, name):
        
            
        def addLine():
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)
        
        tableName = QLabel(name)
        
        table = QTableWidget()
        table.setObjectName(path + " el")
        
        n = len(listChampTable)
        table.setRowCount(1)
        table.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append(listChampTable[i][0]+ "\n(" + listChampTable[i][1]+")")
        table.setHorizontalHeaderLabels(columns)
        
        table.move(0, 0)
        
        completeLayout = QVBoxLayout()
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(table)
        tabLayout.addWidget(addButton)
        
        completeLayout.addWidget(tableName)
        completeLayout.addLayout(tabLayout)
        self.mainLayout.addLayout(completeLayout)
        
    def extraireDonneesEtTypes(self): 
        """parcourt les diff widget de l'espace, on stock dans un dico le nom le widget et le type, retrouve tt les widget enfant de type QCheckBox"""
        donnees_et_types = {}
        for edit in self.findChildren(QLineEdit):
            infos = edit.objectName().split()
            donnees_et_types[infos[0]] = (edit.text(), infos[1])
    
        for combobox in self.findChildren(QComboBox):
            infos = combobox.objectName().split()
            donnees_et_types[infos[0]] = (combobox.currentText(), infos[1])

        
        for tablewidget in self.findChildren(QTableWidget):
            table = []
            headers = []
            for col in range(tablewidget.columnCount()) :
                header = tablewidget.horizontalHeaderItem(col).text()
                if "\n" in header :
                    header2 = header.split("\n")
                    nameColumn = header2[0]
                    typeColumn = header2[1][1:-1]
                    headers.append((nameColumn,typeColumn))
                else :
                    headers.append(header[1:-1])
            table.append(headers)
            
                
            for row in range(tablewidget.rowCount()):
                data = []
                for col in range(tablewidget.columnCount()):
                    it = tablewidget.item(row, col)
                    text = it.text() if it is not None else ""
                    data.append(text)
                table.append(data)
            donnees_et_types[tablewidget.objectName().split()[0]] = (table, 'el')
    
        print(donnees_et_types)
        

if __name__ == "__main__":
    
    champ1 = Champ("Number", ["int"], ".../Number")
    champ2 = Champ("Id", ["int"], ".../Id")
    champ3 = Champ("Name", ["string", "string"],".../Name")
    champ4 = Champ("Number", ["int"], "haha/el/Number")
    champ5 = Champ("Id", ["int"], "haha/el/Id")
    champ6 = Champ("Name", ["string"], "haha/el/Name")
    champ8 = Champ("Number", ["int"], "héhé/el/Number")
    champ9 = Champ("Id", ["int"], "héhé/el/Id")
    champ10 = Champ("Arg", ["string"],".../Arg")
    champ11 = Champ("AAAARRRRGG", ["Float","Float"],"hoho/el")
    champ12 = Champ("Truc", ["string", "enum_SysCoGeo"],".../Truc")
    
    champ7 = Champ("SystemeDeCoordonnées", ["enum_SysCoGeo"], "num/nim/SystemeDeCoordonnées")
    champs= [champ1, champ2,champ3, champ7, champ4, champ5, champ6, champ8, champ9, champ10, champ12, champ11]
    
    app = QApplication(sys.argv)
    gui = XmlEditorGUI(champs)
    gui.show()
    sys.exit(app.exec_())