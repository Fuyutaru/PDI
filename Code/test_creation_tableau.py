# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:05:11 2024

@author: Svetie
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog, QApplication
from Champ import Champ

class Tableau(QDialog):
    def __init__(self, champs):
        super(Tableau, self).__init__()
        self.listeChamps = champs
        self.addButton = QPushButton("+")
        self.addButton.clicked.connect(self.addLine)

        
        self.createTable()
        
        self.tabLayout = QHBoxLayout()
        self.tabLayout.addWidget(self.tableau)
        self.tabLayout.addWidget(self.addButton)
        self.setLayout(self.tabLayout)
        
        
    def createTable(self):
        self.tableau = QTableWidget()
        
        self.tableau.setRowCount(1)
        self.tableau.setColumnCount(len(self.listeChamps))
        columns = []
        for i in range(len(self.listeChamps)) :
            columns.append(self.listeChamps[i].nom)
        self.tableau.setHorizontalHeaderLabels(columns)
        
        self.tableau.move(0, 0)
    
    def addLine(self):
        rowPosition = self.tableau.rowCount()
        self.tableau.insertRow(rowPosition)
        
        
champ1 = Champ("Number", "int", 1)
champ2 = Champ("Id", "int", 2)
champ3 = Champ("Name", "string", 3)
champs= [champ1, champ2, champ3]
        
# main
app = QApplication(sys.argv)
mainwindow = Tableau(champs)
mainwindow.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")