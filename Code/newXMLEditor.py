
"""
A partir de mon code, je souhaite faire en sorte que lorsque l'on charge un fichier de donnée, les informatons de celui ci apparaissent correctement dans les champs? Comment faire(théoriquement sous forme d'etape stp)?

J'avais imaginer les etape suivante:
    Etape 1:charger le fichiers de specif
    Etape 2: charger le fichier de donnée
    Etape 3: création d'une fonction permettant de verifier le fichier de specification selectionner
    Etape 4 recuperation des donnée du fichier d'entre
    Etape 5: fonction permettant d'integrer ses information dans le champs.
    
    c'est etape sont elles suffisante, quelle fonction rajouter?' developpe ta reflexion su mon code
    
    (Attention les informations recuperer = liste de classe champ,qui contient chaque balise unitaire (ouverte , fermer) et qui contient chaque ligne du tableau si xml de data fournit), liste avec obj de la classe champs, ajouter des lignes au tableau car defois fichiers preremplis

ennonce les etapes a réaliser et les fonctions a créer pour permettre/mdoifier cela à partir de mon code
    
"""

import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem

import data_handling as dh
import FileLoader
import Enumeration
from Field import Field
from XmlManager import XmlManager
from DataType import DataType

class XmlEditorGUI(QMainWindow):
    def __init__(self): #Champs sera a retirer quand on aura la conversion
                                #des fichiers XML en liste de champs
        super().__init__()
        self.specification_xml_path = None
        self.data_xml_path = None
        self.specification_xml_structure = None
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        
        #TEST D'AJOUT DES CHAMPS
        
        self.champs = None

    
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
        #met la fct de tchek/verif la direct
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de spécification XML', '', 'XML files (*.xml)')
        if path:
            self.specification_xml_path = path
            tree = ET.parse(self.specification_xml_path)
            strat = XmlManager()
            # self.specification_xml_structure = dh.analyzeSpecification(tree)
            if (strat.verif(tree) == True):
                specif = DataType(strat, self.specification_xml_path)
                print(self.specification_xml_path)
                specif.readFile()
                self.specification_xml_structure = specif
                print(self.specification_xml_path)
                print(self.specification_xml_structure)
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
            

    def onFileLoaded(self, data):#add traitement
    #Récupération des données du fichier d'entrée :lois
        self.textEdit.setText(data)
        QMessageBox.information(self, 'Succès', 'Fichier de données XML chargé avec succès!')


#xml manager, convert to filed, crzation class, readfile , xml.create data en l'assoc list champ  = xml.converttofile'

    def integrerInformationsChamps(self, donnees):
        # on parcourt tt les champ et on tcjeck si balise el, on regard esi l'indice est valide
        # on remplis les champs(si champ normal->)
        # on tcheck si le champs est en lien avec une clé de enumDict, si yes on remplis champs avec QComboBox et on l'add au layout
        # on voit si l'indice est correct, selection option dans QComboBox puis add layout
        #si champs pas enumDict c'est un cas QLineEdit et on refait la meme
        
        for i, champ in enumerate(self.champs):
            if champ.balise == "el":
                if i < len(donnees):
                    champ.setValeur(donnees[i])
            else:
                if champ.type in Enumeration.enumDict:
                        enumComboBox = QComboBox()
                        enumComboBox.addItems(Enumeration.enumDict[champ.type])
                        if i < len(donnees):
                            enumComboBox.setCurrentText(donnees[i])
                        enumLayout = QHBoxLayout()
                        nom = QLabel(champ.nom)
                        enumLayout.addWidget(nom)
                        enumLayout.addWidget(enumComboBox)
                        typeEnum = QLabel("(" + champ.type + ")")
                        enumLayout.addWidget(typeEnum)
                        self.mainLayout.addLayout(enumLayout)
                else:
                    if i < len(donnees):
                        champLayout = QHBoxLayout()
                        nom = QLabel(champ.nom)
                        champLayout.addWidget(nom)
                        champLineEdit = QLineEdit()
                        champLineEdit.setText(donnees[i])
                        champLayout.addWidget(champLineEdit)
                        typeChamp = QLabel("(" + champ.type + ")")
                        champLayout.addWidget(typeChamp)
                        self.mainLayout.addLayout(champLayout)


    def afficherInformations(self):
        for i, champ in enumerate(self.champs):
            if champ.balise == "el":
                widget = self.mainLayout.itemAt(i)
                if isinstance(widget, QHBoxLayout):
                    line_edit = widget.itemAt(1).widget()
                    line_edit.setText(champ.getValeur())
            else:
                widget_layout = self.mainLayout.itemAt(i)
                if isinstance(widget_layout, QHBoxLayout):
                    widget = widget_layout.itemAt(1).widget()
                    if isinstance(widget, QComboBox):
                        index = widget.findText(champ.getValeur())
                        if index != -1:
                            widget.setCurrentIndex(index)
                    elif isinstance(widget, QLineEdit):
                        widget.setText(champ.getValeur())


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
    
    champ1 = Field("Number", "int", 1)
    champ2 = Field("Id", "int", 2)
    champ3 = Field("Name", "string", 3)
    champ4 = Field("Number", "int", "el")
    champ5 = Field("Id", "int", "el")
    champ6 = Field("Name", "string", "el")
    champ7 = Field("Systeme de coordonnées", "enum_SysCoGeo", 4)
    champs= [champ1, champ2, champ4, champ5, champ6, champ3, champ7, champ4, champ5]
    
    app = QApplication(sys.argv)
    gui = XmlEditorGUI(champs)
    gui.show()
    sys.exit(app.exec_())