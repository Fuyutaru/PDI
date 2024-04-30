# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:20:57 2024

@author: Laurie
"""

from Champ import Champ
import sys
from PyQt5.QtWidgets import QApplication
from GUIM import GUIM

app = QApplication(sys.argv)

champ1 = Champ("Number", "int", 1)
champ2 = Champ("Id", "int", 2)
champ3 = Champ("Name", "string", 3)
champ4 = Champ("Number", "int", "el")
champ5 = Champ("Id", "int", "el")
champ6 = Champ("Name", "string", "el")
champ7 = Champ("Systeme de coordonnées", "enum_SysCoGeo", 4)
champs= [champ1, champ2, champ4, champ5, champ6, champ3, champ7, champ4, champ5]

window = GUIM(champs)
window.show()

app.exec()