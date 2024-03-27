# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:27:35 2024

@author: Svetie
"""

from GUI import GUI
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

champs= []

window = GUI(champs)
window.show()

app.exec()