# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:43:14 2024

@author: Svetie
"""

from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import QSize, Qt

import sys

class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Création formulaire avec un bouton")
        self.formGroupXML= QGroupBox("Fichiers XML")
        self.bouton = QPushButton("OK")
 
        # adding action when form is accepted
        self.bouton.clicked.connect(self.createForm2)
        
        self.mainLayout = QVBoxLayout()
 
        # adding form group box to the layout
        self.mainLayout.addWidget(self.formGroupXML)
 
        # adding button box to the layout
        self.mainLayout.addWidget(self.bouton)
 
        # setting lay out
        self.setLayout(self.mainLayout)
        layout = QFormLayout()
 
        # adding rows
        layout.addRow(QLabel("Créer le formulaire"), self.bouton)
 
        # setting layout
        self.formGroupXML.setLayout(layout)
 
        
        
        
        
    def createForm2(self):
        
        self.bouton.setEnabled(False)
           
        self.formGroupBox = QGroupBox("A remplir")
        
        self.form1 = QLineEdit()
        self.form2 = QLineEdit()
        self.form3 = QLineEdit()
        
        
        donnee1 = QLabel("Donnée 1")
        donnee2 = QLabel("Donnée 2")
        donnee3 = QLabel("Donnée 3")
        t1 = QLabel("(type 1)")
        t2 = QLabel("(type 2)")
        t3 = QLabel("(type 3)")
        
        
        bouton = QPushButton(text="Enregistrer")
        
        lh1 = QHBoxLayout()
        lh2 = QHBoxLayout()
        lh3 = QHBoxLayout()
        
        lh1.addWidget(donnee1)
        lh1.addWidget(self.form1)
        lh1.addWidget(t1)
            
        lh2.addWidget(donnee2)
        lh2.addWidget(self.form2)
        lh2.addWidget(t2)
    
        lh3.addWidget(donnee3)
        lh3.addWidget(self.form3)
        lh3.addWidget(t3)
        
        lfinal = QVBoxLayout()
        
        lfinal.addLayout(lh1)
        lfinal.addLayout(lh2)
        lfinal.addLayout(lh3)
        
        self.formGroupBox.setLayout(lfinal)
        self.mainLayout.addWidget(self.formGroupBox)
 
        # setting lay out
        self.setLayout(self.mainLayout)
        

app = QApplication(sys.argv)

window = Window()
window.show()

app.exec()