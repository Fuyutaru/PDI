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
        
    def save():
        pass
    
    def ajouterChamp():
        pass
    
    def ajouterTab():
        pass