# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:53:04 2024

@author: Svetie
"""


import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,  QStandardItemModel, QStandardItem

from DataType import DataType
from XmlManager import XmlManager
import data_handling as dh
import FileLoader
from Enumeration import enum
from Field import Field
from XmlManager import XmlManager

class XmlEditorGUI(QMainWindow):
    def __init__(self): #Champs sera a retirer quand on aura la conversion
                                #des fichiers XML en liste de champs
        super().__init__()
        self.specification_xml_path = None
        self.data_xml_path = None
        self.specification_xml_structure = None
        self.data_xml_structure = None
        self.saveButton = QPushButton()
        self.mainLayout = QVBoxLayout()
        self.fields = None
        
        self.count = 0
        
        self.countTable = 0
        
        #TEST D'AJOUT DES CHAMPS
   
    

    
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

        # Buttons
        saveButton = QPushButton(QIcon('./icon.png'), 'Sauvegarder', self)
        #saveButton.clicked.connect(self.saveDataXml)
        saveButton.clicked.connect(self.extraireDonneesEtTypes)
        saveButton.setToolTip('Sauvegarder le fichier XML')
        saveButton.setObjectName("Save")

        # Layouts
        self.mainLayout = QVBoxLayout()
        # self.mainLayout.addWidget(self.textEdit)
        

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(saveButton)
        self.mainLayout.addLayout(buttonsLayout)
        

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
            
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
                specif.readFile()
                self.specification_xml_structure = specif
                data_empty = self.specification_xml_structure.createData()
                self.fields = self.specification_xml_structure.convert2Field(data_empty.content)
                if self.count > 0 :
                    self.deleteLayout()
                self.addFields()
                self.count += 1
            else:
                QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de spécification.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de spécification.')

    def loadDataXml(self):
        if self.specification_xml_structure == None :
            QMessageBox.warning(self, 'Erreur', 'Un fichier de spécification doit être chargé avant de charger un fichier de données')
        else :
            path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de données XML', '', 'XML files (*.xml)')
            if path:
                self.data_xml_path = path
                
                # self.loader = FileLoader(path)
                # self.loader.fileLoaded.connect(self.onFileLoaded)
                # self.loader.start()
                
                tree = ET.parse(self.data_xml_path)
                strat = XmlManager()
            
                if (strat.verif(tree) == True):
                    data = DataType(strat, self.data_xml_path)
                    data.readFile()
                    self.data_xml_structure = data
                    self.setDataInField()
                    print(self.fields[4].value)
                    
                    QMessageBox.information(self, 'Succès', 'Fichier de spécification chargé avec succès!')
                else:
                    QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de spécification.')
            else:
                QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de spécification.')
            

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
    
    def deleteLayout(self):
        
        for button in self.findChildren(QPushButton):
            if button.objectName() != "Save" :
                button.setParent(None)
        
        for label in self.findChildren(QLabel):
            label.setParent(None)
        
        for edit in self.findChildren(QLineEdit):
            edit.setParent(None)
    
        for combobox in self.findChildren(QComboBox):

            combobox.setParent(None)
        
        for tablewidget in self.findChildren(QTableWidget):
            
            tablewidget.setParent(None)
        
    
    def addFields(self):
        
        listFieldTable = []
        n = len(self.fields)
        for i in range(n):
            typeField = self.fields[i].type
            pathField = self.fields[i].path
            pathFieldSplit = self.fields[i].path.split("/")
            pathFieldSplitNext = []
            
            
            if i < n-1 :
                pathFieldSplitNext = self.fields[i+1].path.split("/")
            
            if pathFieldSplit[-1] == "el" :
                self.addTable(pathFieldSplit[-2], pathField, typeField)            
                        
            elif pathFieldSplit[-2] == "el" :
                if i == n-1 or (pathFieldSplit[:-1] != pathFieldSplitNext[:-1]) :
                    listFieldTable.append([pathFieldSplit[-1], typeField[0]])
                    name = pathFieldSplit[-3]
                    path = pathField[:-(len(pathFieldSplit[-1])+1)]
                    self.addFieldTable(listFieldTable, path, name)
                    listFieldTable = []
                    
                else :
                    listFieldTable.append([pathFieldSplit[-1], typeField[0]])
            
            elif len(typeField) != 1 :
                name = QLabel(pathFieldSplit[-1])
                multiTypeLayout = QHBoxLayout()
                multiTypeLayout.addWidget(name)
                for t in typeField :
                    if t.strip('"') in enum.enumDict :
                        t = t.strip('"')
                        enumComboBox = QComboBox()
                        enumComboBox.addItems(enum.enumDict[t])
                        enumComboBox.setObjectName(pathField +  " " + t)
                        enumLayout = QHBoxLayout()
                        enumLayout.addWidget(enumComboBox)
                        typeEnum = QLabel("(" + t + ")")
                        enumLayout.addWidget(typeEnum)
                        multiTypeLayout.addLayout(enumLayout)
                    else :
                        fieldLayout = QHBoxLayout()
                        field = QLineEdit()
                        field.setObjectName(pathField + " " + t)
                        fieldLayout.addWidget(field)
                        typeField = QLabel("(" + t + ")")
                        fieldLayout.addWidget(typeField)
                        multiTypeLayout.addLayout(fieldLayout)
                        
                self.mainLayout.addLayout(multiTypeLayout)
                
                        
                        
            
            elif typeField[0].strip('"') in enum.enumDict :
                t = typeField[0].strip('"')
                enumComboBox = QComboBox()
                enumComboBox.addItems(enum.enumDict[t])
                enumComboBox.setObjectName(pathField + " " + t)
                enumLayout = QHBoxLayout()
                nom = QLabel(pathFieldSplit[-1])
                enumLayout.addWidget(nom)
                enumLayout.addWidget(enumComboBox)
                typeEnum = QLabel("(" + t + ")")
                enumLayout.addWidget(typeEnum)
                self.mainLayout.addLayout(enumLayout)
            
            
            else :
                fieldLayout = QHBoxLayout()
                nom = QLabel(pathFieldSplit[-1])
                field = QLineEdit()
                field.setObjectName(pathField + " " + typeField[0])
                fieldLayout.addWidget(nom)
                fieldLayout.addWidget(field)
                typeField = QLabel("(" + typeField[0] + ")")
                fieldLayout.addWidget(typeField)
                self.mainLayout.addLayout(fieldLayout)
        
        scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        widget = QWidget()
        self.mainLayout.addStretch()
        widget.setLayout(self.mainLayout)
        
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        self.setCentralWidget(scroll)
        
        self.setLayout(self.mainLayout)
        
    
    def addTable(self, name, path, types):
        
        def addLine():
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)
        
        
        tableName = QLabel(name)
        
        table = QTableWidget()
        table.setObjectName(path + " el")
        
        n = len(types)
        table.setRowCount(1)
        table.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append("(" + types[i] + ")")
        table.setHorizontalHeaderLabels(columns)
        
        table.move(0, 0)
        
        completeLayout = QVBoxLayout()
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(table)
        tabLayout.addWidget(addButton)
        
        completeLayout.addWidget(tableName)
        completeLayout.addLayout(tabLayout)
        self.mainLayout.addLayout(completeLayout)
        
        
        
    
    def addFieldTable(self, listFieldTable, path, name):
        
            
        def addLine():
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)
        
        tableName = QLabel(name)
        
        table = QTableWidget()
        table.setObjectName(path + " el")
        
        n = len(listFieldTable)
        table.setRowCount(1)
        table.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append(listFieldTable[i][0]+ "\n(" + listFieldTable[i][1]+")")
        table.setHorizontalHeaderLabels(columns)
        
        table.move(0, 0)
        
        completeLayout = QVBoxLayout()
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(table)
        tabLayout.addWidget(addButton)
        
        completeLayout.addWidget(tableName)
        completeLayout.addLayout(tabLayout)
        self.mainLayout.addLayout(completeLayout)
        
    def extraireDonneesEtTypes(self): 
        """parcourt les diff widget de l'espace, on stock dans un dico le nom le widget et le type, retrouve tt les widget enfant de type QCheckBox"""
        donnees_et_types = {}
        for edit in self.findChildren(QLineEdit):
            infos = edit.objectName().split()
            if infos[0] in donnees_et_types :
                donnees_et_types[infos[0]] = ( donnees_et_types[infos[0]][0]+ " " + edit.text(),  donnees_et_types[infos[0]][1] + " " + infos[1])
            else :
                donnees_et_types[infos[0]] = (edit.text(), infos[1])
    
        for combobox in self.findChildren(QComboBox):
            infos = combobox.objectName().split()
            donnees_et_types[infos[0]] = (combobox.currentText(), infos[1])

        
        for tablewidget in self.findChildren(QTableWidget):
            table = []
            headers = []
            for col in range(tablewidget.columnCount()) :
                header = tablewidget.horizontalHeaderItem(col).text()
                if "\n" in header :
                    header2 = header.split("\n")
                    nameColumn = header2[0]
                    typeColumn = header2[1][1:-1]
                    headers.append((nameColumn,typeColumn))
            table.append(headers)
            self.data_xml_structure
                
            for row in range(tablewidget.rowCount()):
                data = []
                for col in range(tablewidget.columnCount()):
                    it = tablewidget.item(row, col)
                    text = it.text() if it is not None else ""
                    data.append(text)
                table.append(data)
            donnees_et_types[tablewidget.objectName().split()[0]] = (table, 'el')
    
        print(len(donnees_et_types))
        
    def setDataInField(self):
        list_t, list_d, a, b = self.data_xml_structure.strat.iterate(self.specification_xml_structure, self.data_xml_structure)
        
        
        for data in list_d:
            for field in self.fields:
                if data[0] == ('Root' + field.path): #ATTENTION ROOT!!!
                    if "el" in data[0]:
                        if field.value == ['']:
                            field.value = data[1]
                        else:
                            i = self.fields.index(field)
                            new_field = Field(field.name, field.type, field.path, data[1])
                            self.fields.insert(i+1, new_field)
                            
                    else:
                        if isinstance(data[1],list):
                            field.value = data[1]
                        else:
                            field.value = [data[1]]
        

if __name__ == "__main__":
    
    # Test your XML class
    xmlStrat = XmlManager()
    xml = DataType(xmlStrat,"example/FullSpecif.xml")
    Dataxml = DataType( xmlStrat,"example/Data_FullSpecif.xml")
    xml.readFile()
    Dataxml.readFile()
    
    # for el in Dataxml.content.iter() :
    #     print(el.getroottree().getpath(el))
    data_empty = xml.createData()
    # data_empty.convert2File()

    field_list = xml.convert2Field(data_empty.content)

    
    
    
    field1 = Field("Number", ["int"], ".../Number","")
    field2 = Field("Id", ["int"], ".../Id","")
    field3 = Field("Name", ["string", "string"],".../Name","")
    field4 = Field("Number", ["int"], "haha/el/Number","")
    field5 = Field("Id", ["int"], "haha/el/Id","")
    field6 = Field("Name", ["string"], "haha/el/Name","")
    field8 = Field("Number", ["int"], "héhé/el/Number","")
    field9 = Field("Id", ["int"], "héhé/el/Id","")
    field10 = Field("Arg", ["string"],".../Arg","")
    field11 = Field("AAAARRRRGG", ["Float","Float"],"hoho/el","")
    field12 = Field("Truc", ["string", "enum_SysCoGeo"],".../Truc","")
    
    field7 = Field("SystemeDeCoordonnées", ["enum_SysCoGeo"], "num/nim/SystemeDeCoordonnées","")
    fields= [field1, field2,field3, field7, field4, field5, field6, field8, field9, field10, field12, field11]
    
    app = QApplication(sys.argv)
    gui = XmlEditorGUI()
    gui.show()
    sys.exit(app.exec_())