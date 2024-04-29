import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem

import data_handling as dh
import FileLoader
import Enumeration
from Champ import Champ

class XmlEditorGUI(QMainWindow):
    def __init__(self, champs): #Champs sera a retirer quand on aura la conversion
                                #des fichiers XML en liste de champs
        super().__init__()
        self.specification_xml_path = None
        self.data_xml_path = None
        self.specification_xml_structure = None
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        
        #TEST D'AJOUT DES CHAMPS
        
        self.champs = champs
        
    

    
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

        # # Text Editor
        # self.textEdit = QTextEdit(self)
        # self.textEdit.setStyleSheet("QTextEdit {border: 1px solid black; background-color: #f0f0f0;}")

        # Buttons
        saveButton = QPushButton(QIcon('./icon.png'), 'Sauvegarder', self)
        saveButton.clicked.connect(self.saveDataXml)
        saveButton.setToolTip('Sauvegarder le fichier XML')

        # Layouts
        self.mainLayout = QVBoxLayout()
        # self.mainLayout.addWidget(self.textEdit)
        
        ####TEST CHAMPS####
        self.bouton = QPushButton("Ajouter champs")
        self.bouton.clicked.connect(self.ajouterChamps)
        self.mainLayout.addWidget(self.bouton)
        ####TEST CHAMPS####

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(saveButton)
        self.mainLayout.addLayout(buttonsLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
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
            tree = ET.parse(self.data_xml_path)
            root = tree.getroot()
            self.displayXmlData(root)
            QMessageBox.information(self, 'Succès', 'Fichier de données XML chargé avec succès!')
        else:
            QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de données.')



    def displayXmlData(self, root):
        for champ in self.champs:
        # Pour chaque champ, trouver la correspondance dans le fichier XML et mettre à jour l'interface
        # Ceci est une simplification. Vous devrez adapter en fonction de la structure de vos données XML.
            value = root.find(champ.nom)
            if value is not None and isinstance(getattr(self, champ.nom, None), QLineEdit):
                getattr(self, champ.nom).setText(value.text)
            elif value is not None and isinstance(getattr(self, champ.nom, None), QComboBox):
                 getattr(self, champ.nom).setCurrentText(value.text)

    def displayXmlData(self, root):
        for champ in self.champs:
            element = root.find(champ.nom)
            if element is not None and champ.nom in self.widgets:
                widget = self.widgets[champ.nom]
                if isinstance(widget, QLineEdit):
                    widget.setText(element.text)
                elif isinstance(widget, QComboBox):
                    index = widget.findText(element.text)
                    if index != -1:
                        widget.setCurrentIndex(index)


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
    
    def ajouterChamps(self):
        listeChampTableau = []
        n = len(self.champs)
        for i in range(n):
            if self.champs[i].balise == "el" :
                if i == n-1 or (i < n-1 and self.champs[i+1].balise != "el"):
                    listeChampTableau.append(self.champs[i])
                    self.ajouterTab(listeChampTableau)
                    listeChampTableau = []
                else :
                    listeChampTableau.append(self.champs[i])
            elif self.champs[i].type in Enumeration.enumDict :
                enumComboBox = QComboBox()
                enumComboBox.addItems(Enumeration.enumDict[self.champs[i].type])
                
                enumLayout = QHBoxLayout()
                nom = QLabel(self.champs[i].nom)
                enumLayout.addWidget(nom)
                enumLayout.addWidget(enumComboBox)
                typeEnum = QLabel("(" + self.champs[i].type + ")")
                enumLayout.addWidget(typeEnum)
                self.mainLayout.addLayout(enumLayout)
            else :
                champLayout = QHBoxLayout()
                nom = QLabel(self.champs[i].nom)
                champLayout.addWidget(nom)
                champLayout.addWidget(QLineEdit())
                typeChamp = QLabel("(" + self.champs[i].type + ")")
                champLayout.addWidget(typeChamp)
                self.mainLayout.addLayout(champLayout)
                
        self.setLayout(self.mainLayout)
        
    def ajouterChamps(self):
        self.widgets = {}  # Dictionnaire pour conserver une référence aux widgets par nom de champ
        listeChampTableau = []
        n = len(self.champs)

        for i in range(n):
            if self.champs[i].balise == "el":
                if i == n-1 or (i < n-1 and self.champs[i+1].balise != "el"):
                    listeChampTableau.append(self.champs[i])
                    self.ajouterTab(listeChampTableau)
                    listeChampTableau = []
                else:
                    listeChampTableau.append(self.champs[i])
            elif self.champs[i].type in Enumeration.enumDict:
                            enumComboBox = QComboBox()
                            enumComboBox.addItems(Enumeration.enumDict[self.champs[i].type])
                            
                            enumLayout = QHBoxLayout()
                            nom = QLabel(self.champs[i].nom)
                            enumLayout.addWidget(nom)
                            enumLayout.addWidget(enumComboBox)
                            self.widgets[self.champs[i].nom] = enumComboBox  # Enregistre le QComboBox dans le dictionnaire
                            
                            typeEnum = QLabel("(" + self.champs[i].type + ")")
                            enumLayout.addWidget(typeEnum)
                            self.mainLayout.addLayout(enumLayout)
            else:
                champLayout = QHBoxLayout()
                nom = QLabel(self.champs[i].nom)
                
                champLayout.addWidget(nom)
                                
                lineEdit = QLineEdit()
                champLayout.addWidget(lineEdit)
                self.widgets[self.champs[i].nom] = lineEdit  # Enregistre le QLineEdit dans le dictionnaire
                                
                typeChamp = QLabel("(" + self.champs[i].type + ")")
                champLayout.addWidget(typeChamp)
                self.mainLayout.addLayout(champLayout)
                                
                self.setLayout(self.mainLayout)
    
            
            
            
            
            
    def ajouterTab(self, listeChampTableau):
            
            
        def addLine():
            rowPosition = tableau.rowCount()
            tableau.insertRow(rowPosition)
            
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)

        
        tableau = QTableWidget()
        
        n = len(listeChampTableau)
        tableau.setRowCount(1)
        tableau.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append(listeChampTableau[i].nom)
        tableau.setHorizontalHeaderLabels(columns)
        
        tableau.move(0, 0)
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(tableau)
        tabLayout.addWidget(addButton)
        self.mainLayout.addLayout(tabLayout)

if __name__ == "__main__":
    
    champ1 = Champ("Number", "int", 1)
    champ2 = Champ("Id", "int", 2)
    champ3 = Champ("Name", "string", 3)
    champ4 = Champ("Number", "int", "el")
    champ5 = Champ("Id", "int", "el")
    champ6 = Champ("Name", "string", "el")
    champ7 = Champ("Systeme de coordonnées", "enum_SysCoGeo", 4)
    champs= [champ1, champ2, champ4, champ5, champ6, champ3, champ7, champ4, champ5]
    
    app = QApplication(sys.argv)
    gui = XmlEditorGUI(champs)
    gui.show()
    sys.exit(app.exec_())
    
    
