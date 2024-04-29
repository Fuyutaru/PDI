# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:55:19 2024

@author: Svetie
"""


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt


class GUI(QDialog, QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        self.countTable = 0
        
        champLayout = QHBoxLayout()
        nom = QLabel("Nom")
        champLayout.addWidget(nom)
        champ = QLineEdit()
        champ.setObjectName("Nom string") ######Donner un nom aux objets !!!!!!!
        champLayout.addWidget(champ)
        
        typeChamp = QLabel("(string)")
        champLayout.addWidget(typeChamp)
        self.mainLayout.addLayout(champLayout)
        
        enumComboBox = QComboBox()
        enumComboBox.addItems(["TSI", "PPMD", "IGAST", "Cartagéo","DDMEG"])
        enumLayout = QHBoxLayout()
        nom = QLabel("Filière")
        enumComboBox.setObjectName("Filiere Enum")
        enumLayout.addWidget(nom)
        enumLayout.addWidget(enumComboBox)
        typeEnum = QLabel("(string)")
        enumLayout.addWidget(typeEnum)
        self.mainLayout.addLayout(enumLayout)
        
        champLayout = QHBoxLayout()
        nom = QLabel("Nombre préféré")
        champLayout.addWidget(nom)
        champ = QLineEdit()
        champ.setObjectName("NombrePrefere int")
        champLayout.addWidget(champ)
        typeChamp = QLabel("(int)")
        champLayout.addWidget(typeChamp)
        self.mainLayout.addLayout(champLayout)
        
        listeChampTableau = ["Pokémon string","Type string", "Surnom string"]
        self.ajouterTab(listeChampTableau)
        
        
        self.bouton = QPushButton("Sauvegarder")
        self.bouton.clicked.connect(self.extraireDonneesEtTypes)
        self.mainLayout.addWidget(self.bouton)
        
        self.setLayout(self.mainLayout)
        
    
    def extraireDonneesEtTypes(self): 
        """parcourt les diff widget de l'espace, on stock dans un dico le nom le widget et le type, retrouve tt les widget enfant de type QCheckBox"""
        donnees_et_types = {}
        for Champ in self.findChildren(QLineEdit):
            infos = Champ.objectName().split()
            donnees_et_types[infos[0]] = (Champ.text(), infos[1])
    
        for Champ in self.findChildren(QComboBox):
            infos = Champ.objectName().split()
            donnees_et_types[infos[0]] = (Champ.currentText(), infos[1])

        
        for tablewidget in self.findChildren(QTableWidget):
            table = []
            headers = []
            for col in range(tablewidget.columnCount()) :
                
                header = tablewidget.horizontalHeaderItem(col).text().split("\n")
                nameColumn = header[0]
                typeColumn = header[1][1:-1]
                headers.append((nameColumn,typeColumn))
            table.append(headers)
            
                
            for row in range(tablewidget.rowCount()):
                data = []
                for col in range(tablewidget.columnCount()):
                    it = tablewidget.item(row, col)
                    text = it.text() 
                    data.append(text)
                table.append(data)
            donnees_et_types[tablewidget.objectName()] = (table, 'el')
    
        print(donnees_et_types)
        
     
            
                
            

    def save(self):
        #test = []
        #for i in range(self.layout().count()):
        #    hboxlayout = self.layout().itemAt(i)
        #    for k in range(hboxlayout.layout().count()):
        #        widget = hboxlayout.itemAt(k).widget()
        #        if isinstance(widget, QComboBox):
        #            test.append(widget.currentText())
        #        if isinstance(widget, QLineEdit):
        #            test.append(widget.text())
            #if widget == QTableWidget():
        pass
        
    
    def ajouterTab(self, listeChampTableau):
        
            
        def addLine():
            rowPosition = tableau.rowCount()
            tableau.insertRow(rowPosition)
            
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)
        
        self.countTable += 1
        
        tableau = QTableWidget()
        tableau.setObjectName(f"table{self.countTable}")
        
        n = len(listeChampTableau)
        tableau.setRowCount(1)
        tableau.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append(listeChampTableau[i].split()[0] + "\n(" + listeChampTableau[i].split()[1] + ")" )
        tableau.setHorizontalHeaderLabels(columns)
        
        tableau.move(0, 0)
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(tableau)
        tabLayout.addWidget(addButton)
        self.mainLayout.addLayout(tabLayout)
        
app = QApplication(sys.argv)

window = GUI()
window.show()

app.exec()

