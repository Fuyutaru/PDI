# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:57:27 2024

@author: Svetie
"""

import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QTextEdit, QMessageBox, QStatusBar, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem

import data_handling as dh
import FileLoader

class XmlEditorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.specification_xml_path = None
        self.data_xml_path = None
        self.specification_xml_structure = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Éditeur de Fichiers XML')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('./icone.png'))

        # Barre de menu
        menuBar = self.menuBar()
        menuBar.setStyleSheet("QMenuBar { background-color: #e1e1e1; color: #333333; }")
        fileMenu = menuBar.addMenu('&Fichier')

        # Actions du menu
        loadSpecAction = QAction(QIcon('./icone.png'), 'Charger Spécification', self)
        loadSpecAction.triggered.connect(self.loadSpecificationXml)
        fileMenu.addAction(loadSpecAction)

        loadDataAction = QAction(QIcon('./icone.png'), 'Charger Données XML', self)
        loadDataAction.triggered.connect(self.loadDataXml)
        fileMenu.addAction(loadDataAction)

        # Text Editor
        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet("QTextEdit {border: 1px solid black; background-color: #f0f0f0;}")

        # Buttons
        saveButton = QPushButton(QIcon('./icon.png'), 'Sauvegarder', self)
        saveButton.clicked.connect(self.saveDataXml)
        saveButton.setToolTip('Sauvegarder le fichier XML')

        # Layouts
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.textEdit)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(saveButton)
        mainLayout.addLayout(buttonsLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
                 
# def buildTree(self, parent, element):
#     item_text = element.tag
#     item = self.treeWidget.invisibleRootItem() if parent is None else QTreeWidgetItem(parent)
#     item.setText(0, item_text)

#     item.setFlags(item.flags() & ~Qt.ItemIsEditable)
#     for attrib_name, attrib_value in element.attrib.items():
#         attrib_text = f"{attrib_name}='{attrib_value}'"
#         attrib_item = QTreeWidgetItem(item)
#         attrib_item.setText(0, attrib_text)
#         attrib_item.setFlags(attrib_item.flags() | Qt.ItemIsEditable)

    # for child in element:
    #     self.buildTree(item, child)

    def loadSpecificationXml(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de spécification XML', '', 'XML files (*.xml)')
        if path:
            self.specification_xml_path = path
            tree = ET.parse(self.specification_xml_path)
            self.specification_xml_structure = dh.analyzeSpecification(tree)
            QMessageBox.information(self, 'Succès', 'Fichier de spécification chargé avec succès!')
        else:
            QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de spécification.')

    def loadDataXml(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de données XML', '', 'XML files (*.xml)')
        if path:
            self.data_xml_path = path
            self.loader = FileLoader(path)
            self.loader.fileLoaded.connect(self.onFileLoaded)
            self.loader.start()

    def onFileLoaded(self, data):
        self.textEdit.setText(data)
        QMessageBox.information(self, 'Succès', 'Fichier de données XML chargé avec succès!')

    def saveDataXml(self):
        if dh.validateXml(self.textEdit.toPlainText(), self.specification_xml_structure):
            if not self.data_xml_path:
                path, _ = QFileDialog.getSaveFileName(self, 'Enregistrer le fichier de données XML', '', 'XML files (*.xml)')
                if path:
                    self.data_xml_path = path
            with open(self.data_xml_path, 'w') as file:
                file.write(self.textEdit.toPlainText())
            QMessageBox.information(self, 'Succès', 'Fichier de données XML enregistré avec succès!')
        else:
            QMessageBox.warning(self, 'Erreur', 'Le fichier de données XML contient des erreurs.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = XmlEditorGUI()
    gui.show()
    sys.exit(app.exec_())