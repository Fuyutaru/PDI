# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:31:07 2024

@author: Laurie
"""
import sys
import Champ
from datetime import datetime
import base64
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QTextEdit, QMessageBox, QStatusBar, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem

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
            item.setEditable(False) 
            parent.appendRow(item)
    
            for attrib_name, attrib_value in element.attrib.items():
                attrib_item = QStandardItem(f"{attrib_name}='{attrib_value}'")
                attrib_item.setEditable(True)  # Rendre les attributs éditables
                item.appendRow(attrib_item)
    
            for child in element:
                self.buildTree(item, child)
    
    def loadSpecificationXml(self):
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
        specification = {}
        
        for element in xml_tree.getroot():
            element_name = element.attrib.get('name')
            element_type = element.attrib.get('type', 'string') 
            children = {}
            for child in element:
                child_name = child.tag
                child_attribs = {attr_name: attr_value for attr_name, attr_value in child.attrib.items()}
            
                child_constraints = {
                    'type': child_attribs.get('type', 'string'),
                    'required': child_attribs.get('required', 'false').lower() == 'true',
                  
                }
                
                children[child_name] = child_constraints
            
            specification[element_name] = {
                'type': element_type,
                'children': children,
            }
    
        return specification
    
    def newDataXml(self):
        
        if self.specification_xml_structure is None:
            self.statusBar.showMessage("Veuillez d'abord charger un fichier de spécification XML.", 5000)
            return
        
        if self.specification_xml_structure is None:
            QMessageBox.warning(self, 'Erreur', 'Veuillez d abord charger un fichier de spécification XML.')
            return
        
        self.textEdit.clear()
        root_spec = next(iter(self.specification_xml_structure.values()))
        root_element = ET.Element(root_spec['type'])
        
        for child_name, child_spec in root_spec['children'].items():
            child_element = ET.SubElement(root_element, child_name)
        xml_str = ET.tostring(root_element, encoding='unicode')
        self.textEdit.setText(xml_str)
        self.data_xml_path = None
        
        
 
        
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
        self.textEdit.setText(data)
        self.treeModel.clear()
        xml_root = ET.fromstring(data)
        self.buildTree(self.treeModel.invisibleRootItem(), xml_root)
        self.treeView.expandAll()
        

    def extraireDonneesEtTypes(self): 
        """parcourt les diff widget de l'espace, on stock dans un dico le nom le widget et le type, retrouve tt les widget enfant de type QCheckBox"""
        donnees_et_types = {}
            for Champ in self.findChildren(QLineEdit):
                dataType = getattr(Champ, 'dataType', 'str')  
                donnees_et_types[Champ.objectName()] = (Champ.text(), dataType)
    
            for Champ in self.findChildren(QCheckBox):
                dataType = 'boolean'
                donnees_et_types[Champ.objectName()] = (Champ.isChecked(), dataType)
    
            for Champ in self.findChildren(QComboBox):
                dataType = getattr(Champ, 'dataType', 'enum')
                donnees_et_types[Champ.objectName()] = (Champ.currentText(), dataType)
    
            for Champ in self.findChildren(QDateTimeEdit):
                if getattr(Champ, 'dataType', 'datetime') == 'date':
                    donnees_et_types[Champ.objectName()] = (Champ.date().toString('dd/MM/yyyy'), 'date')
                else:
                    donnees_et_types[Champ.objectName()] = (Champ.dateTime().toString('MM-dd-yyyy HH:mm:ss'), 'datetime')
    
            for Champ in self.findChildren(QTextEdit):  
                dataType = getattr(Champ, 'dataType', 'str')
                if dataType == 'list':
                    list_values = [value.strip() for value in Champ.toPlainText().split(',')]
                    donnees_et_types[Champ.objectName()] = (list_values, 'list')
                elif dataType == 'binary':
                    try:
                        base64_encoded_data = base64.b64encode(Champ.toPlainText().encode())
                        donnees_et_types[Champ.objectName()] = (base64_encoded_data.decode('utf-8'), 'binary')
                    except Exception as e:
                        print(f"Erreur lors de l'encodage en base64 : {str(e)}")

            for Champ in self.findChildren(QLineEdit):
                dataType = getattr(Champ, 'dataType', 'str')
                if dataType in ['id', 'idref']:
                    donnees_et_types[Champ.objectName()] = (Champ.text(), dataType)
    
            return donnees_et_types
    

        
      
    def valider_valeur_entree(self, valeur_entree, type_attendu, enum_values=None):
        if type_attendu not in ['int', 'float', 'str', 'boolean', 'date', 'datetime', 'time', 'enum', 'list', 'binary', 'id', 'idref']:
            return False, "Type spécifié pour la validation non pris en charge."

        try:
            if type_attendu == 'int':
                int(valeur_entree)
                return True, "L'entrée est un entier valide."
            elif type_attendu == 'float':
                float(valeur_entree)
                return True, "L'entrée est un flottant valide."
            elif type_attendu == 'str':
                return True, "L'entrée est une chaîne de caractères valide."
            elif type_attendu == 'boolean':
                if valeur_entree.lower() in ['true', 'false']:
                    return True, "L'entrée est un booléen valide."
                else:
                    return False, "L'entrée n'est pas un booléen valide."
            elif type_attendu == 'date':
                datetime.strptime(valeur_entree, '%d/%m/%Y')
                return True, "L'entrée est une date valide."
            elif type_attendu == 'datetime':
                datetime.strptime(valeur_entree, '%m-%d-%Y %I:%M:%S %p')
                return True, "L'entrée est un datetime valide."
            elif type_attendu == 'time':
                datetime.strptime(valeur_entree, '%H:%M:%S')
                return True, "L'entrée est une heure valide."
            elif type_attendu == 'enum':
                if enum_values is None or valeur_entree not in enum_values:
                    return False, "L'entrée n'est pas une valeur autorisée."
                return True, "L'entrée est une valeur enum valide."
            elif type_attendu == 'list':
                list_values = valeur_entree.split(',')
                if not all(list_values):
                    return False, "La liste contient des valeurs vides."
                return True, "L'entrée est une liste valide."
            elif type_attendu == 'binary':
                base64.b64decode(valeur_entree)
                return True, "L'entrée est une donnée binaire valide."
            elif type_attendu in ['id', 'idref']:
                return True, "L'entrée est un identifiant valide."

        except ValueError as e:
            return False, f"L'entrée n'est pas un(e) {type_attendu} valide(e). Message d'erreur : {str(e)}"

        except Exception as e:
            return False, f"Erreur inattendue lors de la validation : {str(e)}"
        
    #print(valider_entree("123", "int"))
    #print(valider_entree("abc", "int"))  
        

    def on_save_button_clicked(self):
        valeur_entree_int = self.lineEditInt.text()
        valide_int, message_int = self.valider_valeur_entree(valeur_entree_int, 'int')
        if not valide_int:
            QMessageBox.warning(self, 'Erreur', message_int)
            return
    
        valeur_entree_float = self.lineEditFloat.text()
        valide_float, message_float = self.valider_valeur_entree(valeur_entree_float, 'float')
        if not valide_float:
            QMessageBox.warning(self, 'Erreur', message_float)
            return
    
        valeur_entree_str = self.lineEditStr.text()
        valide_str, message_str = self.valider_valeur_entree(valeur_entree_str, 'str')
        if not valide_str:  
            QMessageBox.warning(self, 'Erreur', message_str)
            return
        self.saveDataXml()


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
gui = XmlEditorGUI()
gui.show()
sys.exit(app.exec_())