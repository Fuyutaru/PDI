# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:03:51 2024

@author: Svetie
"""

import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QTextEdit, QMessageBox, QStatusBar, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem

import FileLoader, Champ


class GUI(QMainWindow):
    def __init__(self, champs):
        super(GUI, self).__init__()
        self.champs = champs
        self.saveButton = QPushButton()
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
        saveButton = QPushButton(QIcon('./icon.png'), 'Sauvegarder', self)
        saveButton.clicked.connect(self.saveDataXml)
        saveButton.setToolTip('Sauvegarder le fichier XML')

        # Layout principal
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.textEdit)

        # Layout pour les boutons
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(saveButton)
        mainLayout.addLayout(buttonsLayout)

        # Widget central
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Barre de statut
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        
             
    def buildTree(self, parent, element):
            item = QStandardItem(element.tag)
            item.setIcon(QIcon("./icon.png"))  
            item.setEditable(False)  # Rendre l'élément non-éditable
            parent.appendRow(item)
    
            # Ajout des attributs comme enfants de l'élément
            for attrib_name, attrib_value in element.attrib.items():
                attrib_item = QStandardItem(f"{attrib_name}='{attrib_value}'")
                attrib_item.setEditable(True)  # Rendre les attributs éditables
                item.appendRow(attrib_item)
    
            # Construction récursive
            for child in element:
                self.buildTree(item, child)
  
    
    def loadSpecificationXml(self):
        """J'analyse et je stock la structure du fichier xml"""
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de spécification XML', '', 'XML files (*.xml)')
        if path:
            try:
                self.specification_xml_path = path
                tree = ET.parse(self.specification_xml_path)
                self.specification_xml_structure = self.analyzeSpecification(tree)
                QMessageBox.information(self, 'Succès', 'Fichier de spécification chargé avec succès!')
            except ET.ParseError as e:
                QMessageBox.warning(self, 'Erreur', 'Le fichier de spécification XML est invalide.\n' + str(e))
            except Exception as e:
                QMessageBox.warning(self, 'Erreur', 'Une erreur est survenue lors du chargement du fichier.\n' + str(e))

    

    def analyzeSpecification(self, xml_tree):
        """analyse la strucutre du fichier et stock les infos dans un dico"""
        specification = {}
        
        # Parcourons l'arbre XML et collectons les informations
        for element in xml_tree.getroot():
            # Supposons que chaque élément de spécification contienne un 'name' et un 'type'
            element_name = element.attrib.get('name')
            element_type = element.attrib.get('type', 'string')  # Default type is string
            
            # Collectons les informations sur les enfants (sous-éléments)
            children = {}
            for child in element:
                child_name = child.tag
                child_attribs = {attr_name: attr_value for attr_name, attr_value in child.attrib.items()}
                
                # Ajoutons les contraintes de valeurs, la multiplicité, etc.
                child_constraints = {
                    'type': child_attribs.get('type', 'string'),
                    'required': child_attribs.get('required', 'false').lower() == 'true',
                    # autre contraintes hehe
                }
                
                children[child_name] = child_constraints
            
            specification[element_name] = {
                'type': element_type,
                'children': children,
            }
    
        return specification
    
    
    def newDataXml(self):
        """genere un nv fichier xml et permet à l'utilisateur de le modif"""
        
        if self.specification_xml_structure is None:
            self.statusBar.showMessage("Veuillez d'abord charger un fichier de spécification XML.", 5000)
            return
        
        if self.specification_xml_structure is None:
            QMessageBox.warning(self, 'Erreur', 'Veuillez d abord charger un fichier de spécification XML.')
            return
        self.textEdit.clear()#si racine fichier = premier elmt
        root_spec = next(iter(self.specification_xml_structure.values()))
        root_element = ET.Element(root_spec['type'])
        
        for child_name, child_spec in root_spec['children'].items():
            child_element = ET.SubElement(root_element, child_name)#attribut/elmt sup a add
        xml_str = ET.tostring(root_element, encoding='unicode')
        self.textEdit.setText(xml_str)
        self.data_xml_path = None
 

                
                
    def loadDataXml(self):
        """charge un fichier de données xml, son affichage va dans un QTextEdit"""
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de données XML', '', 'XML files (*.xml)')
        if path:
            try:
                tree = ET.parse(path)
                self.data_xml_path = path
                self.onFileLoaded(ET.tostring(tree.getroot(), encoding='unicode'))
            except ET.ParseError as e:
                QMessageBox.warning(self, 'Erreur', 'Le fichier de données XML est invalide.\n' + str(e))
            except Exception as e:
                QMessageBox.warning(self, 'Erreur', 'Une erreur est survenue lors du chargement du fichier.\n' + str(e))

    def onFileLoaded(self, data):
        """met a jour le QTedit"""
        self.textEdit.setText(data)
        if self.validateXml():
            QMessageBox.information(self, 'Succès', 'Fichier de données XML chargé et validé avec succès!')
        else:
            QMessageBox.warning(self, 'Attention', 'Le fichier de données XML est chargé mais contient des erreurs.')


    def saveDataXml(self):
        if self.validateXml():
            if not self.data_xml_path:
                path, _ = QFileDialog.getSaveFileName(self, 'Enregistrer le fichier de données XML', '', 'XML files (*.xml)')
                if path:
                    self.data_xml_path = path
            with open(self.data_xml_path, 'w') as file:
                file.write(self.textEdit.toPlainText())
            QMessageBox.information(self, 'Succès', 'Fichier de données XML enregistré avec succès!')
        else:
            QMessageBox.warning(self, 'Erreur', 'Le fichier de données XML contient des erreurs.')
                   

    def validateXml(self):
        try:
            root = ET.fromstring(self.textEdit.toPlainText())
            if root.tag != self.specification_xml_structure['root_element_name']:
                QMessageBox.warning(self, 'Erreur', f"L'élément racine {root.tag} ne correspond pas à la spécification.")
                return False

            def validate_element(element, spec):
                if element.tag not in spec:
                    QMessageBox.warning(self, 'Erreur', f"L'élément {element.tag} n'est pas autorisé selon la spécification.")
                    return False
                for attrib_name, attrib_value in element.attrib.items():
                    if attrib_name not in spec[element.tag]['attributes']:
                        QMessageBox.warning(self, 'Erreur', f"L'attribut {attrib_name} de {element.tag} n'est pas autorisé.")
                        return False
                for child in element:
                    if not validate_element(child, spec[element.tag]['children']):
                        return False
                return True

            if not validate_element(root, self.specification_xml_structure):
                return False

            QMessageBox.information(self, 'Succès', 'Le fichier XML est valide selon la spécification.')
            return True
        except ET.ParseError as e:
            QMessageBox.warning(self, 'Erreur', f"Le XML est mal formé.\n{e}")
            return False
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', f"Une erreur est survenue pendant la validation.\n{e}")
            return False
        
        

app = QApplication(sys.argv)
champs = [Champ.Champ("nom", "type", "balise"), Champ.Champ("nom2", "type2", "balise2")]
gui = GUI(champs) 
gui.show()
sys.exit(app.exec_())

        
        
    # def save():
    #     pass
    
    # def ajouterChamp():
    #     pass
    
    # def ajouterTab():
    #     pass