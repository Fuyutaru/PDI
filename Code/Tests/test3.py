# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:43:14 2024

@author: Svetie
"""

from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import QSize, Qt

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test")
        self.formGroupXML= QGroupBox("Fichiers XML")
        self.formGroupBox = QGroupBox("A remplir")
        
        
        
        donnee1 = QLabel("Donnée 1")
        donnee2 = QLabel("Donnée 2")
        donnee3 = QLabel("Donnée 3")
        t1 = QLabel("(type 1)")
        t2 = QLabel("(type 2)")
        t3 = QLabel("(type 3)")
        form1 = QLineEdit()
        form2 = QLineEdit()
        enum = QComboBox()
        enum.addItems(["1", "2", "3", "4", "5"])
        
        bouton = QPushButton(text="Enregistrer")
        
        lh1 = QHBoxLayout()
        lh2 = QHBoxLayout()
        lh3 = QHBoxLayout()
        
        lh1.addWidget(donnee1)
        lh1.addWidget(form1)
        lh1.addWidget(t1)
        
        lh2.addWidget(donnee2)
        lh2.addWidget(form2)
        lh2.addWidget(t2)
        
        lh3.addWidget(donnee3)
        lh3.addWidget(enum)
        lh3.addWidget(t3)
        
        lfinal = QVBoxLayout()
        
        lfinal.addLayout(lh1)
        lfinal.addLayout(lh2)
        lfinal.addLayout(lh3)
        
        widget = QWidget()
        widget.setLayout(lfinal)
        self.setCentralWidget(widget)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()