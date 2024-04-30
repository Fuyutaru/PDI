# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:01:16 2024

@author: Svetie
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import base64
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QDateTimeEdit, QComboBox, QCheckBox, QMessageBox


def analyzeSpecification(xml_tree):
    """ Analyse the specification XML and constructs a structured dictionary from it. """
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

def newDataXml(specification_xml_structure, textEdit):
    """ Generates new XML data based on the specification and displays it for user editing. """
    if not specification_xml_structure:
        return "Please load a specification XML first."
    
    root_spec = next(iter(specification_xml_structure.values()))
    root_element = ET.Element(root_spec['type'])
    
    for child_name, child_spec in root_spec['children'].items():
        child_element = ET.SubElement(root_element, child_name)
    xml_str = ET.tostring(root_element, encoding='unicode')
    textEdit.setText(xml_str)

def validateXml(xml_text, specification_xml_structure):
    """ Validates XML data against the loaded specification. """
    try:
        root = ET.fromstring(xml_text)
        if not validate_element(root, specification_xml_structure):
            return False, "XML does not conform to the specification."
        return True, "XML is valid according to the specification."
    except ET.ParseError as e:
        return False, f"XML is malformed: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred during XML validation: {str(e)}"

def validate_element(element, spec):
    """ Recursively validates each element against the specification. """
    if element.tag not in spec:
        return False
    for child in element:
        if not validate_element(child, spec[element.tag]['children']):
            return False
    return True


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
    

def valider_valeur_entree(valeur_entree, type_attendu, enum_values=None):
    """ Validates input values based on expected types. """
    try:
        if type_attendu == 'int':
            int(valeur_entree)
        elif type_attendu == 'float':
            float(valeur_entree)
        elif type_attendu == 'str':
            str(valeur_entree)  # Just to follow the pattern
        elif type_attendu == 'boolean':
            if valeur_entree.lower() not in ['true', 'false']:
                return False, "Input is not a valid boolean."
        elif type_attendu == 'date':
            datetime.strptime(valeur_entree, '%d/%m/%Y')
        elif type_attendu == 'datetime':
            datetime.strptime(valeur_entree, '%m-%d-%Y %I:%M:%S %p')
        elif type_attendu == 'time':
            datetime.strptime(valeur_entree, '%H:%M:%S')
        elif type_attendu == 'enum':
            if enum_values is None or valeur_entree not in enum_values:
                return False, "Input is not a valid enum value."
        elif type_attendu == 'list':
            if not all(valeur_entree.split(',')):
                return False, "List contains empty values."
        elif type_attendu == 'binary':
            base64.b64decode(valeur_entree)
        elif type_attendu in ['id', 'idref']:
            pass  # Assuming ID/IDREF validation is application-specific
        return True, "Input is valid."
    except ValueError as e:
        return False, f"Input is not a valid {type_attendu}. Error: {str(e)}"
    


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