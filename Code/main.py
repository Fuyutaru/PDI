from XmlEditorGUI import XmlEditorGUI
import sys
from PyQt5.QtWidgets import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = XmlEditorGUI()
    gui.show()
    sys.exit(app.exec_())