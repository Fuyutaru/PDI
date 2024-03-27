# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:03:51 2024

@author: Svetie
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt


import Champ

class GUI(QDialogn, QMainWindow):
    def __init__(self, champs):
        self.champs = champs
        self.saveButton = QPushButton()
        self.addChampButton = QPushButton()