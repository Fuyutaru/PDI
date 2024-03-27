# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:31:07 2024

@author: Laurie
"""


from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QTextEdit, QMessageBox, QStatusBar, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon

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

        # Barre de menu améliorée
        menuBar = self.menuBar()
        menuBar.setStyleSheet("QMenuBar { background-color: #e1e1e1; color: #333333; }")
        fileMenu = menuBar.addMenu('&Fichier')

        # Actions du menu avec des icônes
        loadSpecAction = QAction(QIcon('./icone.png'), 'Charger Spécification', self)
        loadSpecAction.triggered.connect(self.loadSpecificationXml)
        fileMenu.addAction(loadSpecAction)

        loadDataAction = QAction(QIcon('./icone.png'),'Charger Données XML', self)
        loadDataAction.triggered.connect(self.loadDataXml)
        fileMenu.addAction(loadDataAction)

        saveDataAction = QAction('Enregistrer Données XML', self)
        saveDataAction.triggered.connect(self.saveDataXml)
        fileMenu.addAction(saveDataAction)


        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet("QTextEdit {border: 1px solid black; background-color: #f0f0f0;}")

        # Boutons avec des icônes et des tooltips
        saveButton = QPushButton(QIcon('path/to/save_icon.png'), 'Sauvegarder', self)
        saveButton.clicked.connect(self.saveDataXml)
        saveButton.setToolTip('Sauvegarder le fichier XML')

        validateButton = QPushButton(QIcon('path/to/validate_icon.png'), 'Valider XML', self)
        validateButton.clicked.connect(self.validateXml)
        validateButton.setToolTip('Valider la structure du fichier XML')

        # Layout principal
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.textEdit)

        # Layout pour les boutons
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(saveButton)
        buttonsLayout.addWidget(validateButton)
        mainLayout.addLayout(buttonsLayout)

        # Widget central
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Barre de statut
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        