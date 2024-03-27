# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:27:35 2024

@author: Svetie
"""

from GUI import GUI
from Champ import Champ
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

champ1 = Champ("Number", "int", 1)
champ2 = Champ("Id", "int", 2)
champ3 = Champ("Name", "string", 3)
champs= [champ1, champ2, champ3]

window = GUI(champs)
window.show()

app.exec()