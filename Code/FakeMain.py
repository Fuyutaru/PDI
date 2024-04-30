from DataType import DataType
from lxml import etree
from Field import Field
from XmlManager import XmlManager
import os
import Enumeration
from newXMLEditor import XmlEditorGUI
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Gui = XmlEditorGUI()
    Gui.show()  
    sys.exit(app.exec_())
    