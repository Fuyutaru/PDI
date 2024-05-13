# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:37:02 2024

@author: Laurie
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:09:39 2024

@author: Laurie
"""

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
        """
       
        Function used to load and verify a specification XML file selected by the user.

        Args:
           None

        Returns:
           None: The function directly modifies the application state by updating the GUI
                 and does not return any value.

        Raises:
           QMessageBox: Shows an error message if the file cannot be loaded or verified.
        
       
        """
        path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de spécification XML', '', 'XML files (*.xml)')
        if path:
            self.specification_xml_path = path
            tree = ET.parse(self.specification_xml_path)
            strat = XmlManager()
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
        
        """
        
        Function used to load and verify a data XML file selected by the user, comparing it against the previously loaded specification XML.

        Args:
            None

        Returns:
            None: The function directly modifies the application state by updating the GUI
                  and does not return any value.

        Raises:
            QMessageBox: Shows an error message if no specification file is loaded, the data file cannot be loaded,
                         does not match the specification, or cannot be verified.
                         
        """

        if self.specification_xml_structure == None :
            QMessageBox.warning(self, 'Erreur', 'Un fichier de spécification doit être chargé avant de charger un fichier de données')
        else :
            path, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier de données XML', '', 'XML files (*.xml)')
            if path:
                self.data_xml_path = path
                
                tree = ET.parse(self.data_xml_path)
                strat = XmlManager()
            
                if (strat.verif(tree) == True):
                    data = DataType(strat, self.data_xml_path)
                    data.readFile()
                    if (data.compare(self.specification_xml_structure, data) == True):
                        self.data_xml_structure = data
                        self.fields = self.specification_xml_structure.convert2Field(data.content)

                        self.deleteLayout()
                        self.addFieldData()
                    
                        QMessageBox.information(self, 'Succès', 'Fichier de données chargé avec succès!')
                    else:
                        QMessageBox.information(self, 'Erreur', 'Le fichier de données ne correspond pas au fichier de spécification!')
                    
                else:
                    QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de données.')
            else:
                QMessageBox.warning(self, 'Erreur', 'Erreur de chargement du fichier de données.')
            

    def onFileLoaded(self, data):
        """
        
        Function used to update the text edit widget with the data from the loaded XML file.

        Args:
           data (str): The content of the XML file loaded.

        Returns:
           None: Updates the GUI component to display the data and informs the user of the successful loading.
        
        """
   
        self.textEdit.setText(data)
        QMessageBox.information(self, 'Succès', 'Fichier de données XML chargé avec succès!')
        
        

    def saveDataXml(self):
        
        """
        
        Function used to save the modifications made to the XML data back to a file.

        Args:
           None

        Returns:
           None: The function directly modifies files on the disk and updates the user interface
                 with messages indicating success or failure.

        Raises:
           QMessageBox: Shows an error message if the XML data contains errors or cannot be saved.
           
        """
           
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
        
    def addFieldData(self) :
        
        tableData = []
        tableRow = []
        tableNameColumns = []
        tableRowPath = ""
        listFieldTable = []
        n = len(self.fields)
        count = 0
        for i in range(n):
            print(self.fields[i].name, self.fields[i].path,self.fields[i].value)
            typeField = self.fields[i].type
            pathField = self.fields[i].path
            valueField = self.fields[i].value
            nameField = self.fields[i].name
            pathFieldSplit = self.fields[i].path.split("/")
            pathFieldSplitNext = []
            #print(pathFieldSplit)
            
            
            
            if i < n-1 :
                pathFieldSplitNext = self.fields[i+1].path.split("/")
            
            if pathFieldSplit[-1] == "el" :
                tableData.append(valueField)
                if pathFieldSplit != pathFieldSplitNext or i == n-1 :
                    self.addTableData(pathFieldSplit[-2], pathField, typeField, tableData) 
                    tableData=[]
                        
            elif pathFieldSplit[-2] == "el":
                pathFieldWithout = pathFieldSplit
                pathFieldWithout[-2] = pathFieldSplit[-2][:2]
                if tableRowPath == pathFieldWithout:
                    tableData.append(tableRow)
                    tableRow = []
                if count == 0 :
                    tableRowPath = pathFieldWithout
                    count = 1
                if not ((nameField, typeField) in tableNameColumns) :
                    tableNameColumns.append((nameField, typeField))
                tableRow.append(valueField)
                
                # test = False
                # if pathFieldSplit[:-2] != pathFieldSplitNext[:-2] or (pathFieldSplit[-2][:2] !=):
                #     test = True
                
                #print(pathFieldSplit[:-1], pathFieldSplitNext[:-1])
                if i == n-1 or (pathFieldSplit[:-2] != pathFieldSplitNext[:-2]):
                    tableData.append(tableRow)
                    name = pathFieldSplit[-3]
                    path = pathField[:-(len(pathFieldSplit[-1])+1)]
                    self.addFieldTableData(tableNameColumns, path, name, tableData)
                    tableData = []
                    count = 0
                
            
            elif len(typeField) != 1 :
                name = QLabel(pathFieldSplit[-1])
                multiTypeLayout = QHBoxLayout()
                multiTypeLayout.addWidget(name)
                for j in range(len(typeField)):
                    t = typeField[j]
                    v = valueField[j]
                    if t.strip('"') in enum.enumDict :
                        t = t.strip('"')
                        enumComboBox = QComboBox()
                        enumComboBox.addItems(enum.enumDict[t])
                        enumComboBox.setObjectName(pathField +  " " + t)
                        enumComboBox.setCurrentText(v)
                        enumLayout = QHBoxLayout()
                        enumLayout.addWidget(enumComboBox)
                        typeEnum = QLabel("(" + t + ")")
                        enumLayout.addWidget(typeEnum)
                        multiTypeLayout.addLayout(enumLayout)
                    else :
                        fieldLayout = QHBoxLayout()
                        field = QLineEdit()
                        field.setObjectName(pathField + " " + t)
                        field.setText(v)
                        fieldLayout.addWidget(field)
                        typeField2 = QLabel("(" + t + ")")
                        fieldLayout.addWidget(typeField2)
                        multiTypeLayout.addLayout(fieldLayout)
                        
                self.mainLayout.addLayout(multiTypeLayout)
                
                        
                        
            
            elif typeField[0].strip('"') in enum.enumDict :
                t = typeField[0].strip('"')
                v = valueField[0]
                enumComboBox = QComboBox()
                enumComboBox.addItems(enum.enumDict[t])
                enumComboBox.setObjectName(pathField + " " + t)
                enumComboBox.setCurrentText(v)
                enumLayout = QHBoxLayout()
                nom = QLabel(pathFieldSplit[-1])
                enumLayout.addWidget(nom)
                enumLayout.addWidget(enumComboBox)
                typeEnum = QLabel("(" + t + ")")
                enumLayout.addWidget(typeEnum)
                self.mainLayout.addLayout(enumLayout)
            
            
            else :
                fieldLayout = QHBoxLayout()
                v = valueField[0]
                nom = QLabel(pathFieldSplit[-1])
                field = QLineEdit()
                field.setObjectName(pathField + " " + typeField[0])
                field.setText(v)
                fieldLayout.addWidget(nom)
                fieldLayout.addWidget(field)
                typeField2 = QLabel("(" + typeField[0] + ")")
                fieldLayout.addWidget(typeField2)
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
    
    def addFields(self):
        
        listFieldTable = []
        n = len(self.fields)
        for i in range(n):
            #print(self.fields[i].name, self.fields[i].path)
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
        
    def addTableData(self, name, path, types, tableData):
        
        def addLine():
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)
        
        
        tableName = QLabel(name)
        
        table = QTableWidget()
        table.setObjectName(path + " el")
        
        n = len(types)
        l = len(tableData)
        table.setRowCount(l)
        table.setColumnCount(n)
        columns = []
        for i in range(n) :
            columns.append("(" + types[i] + ")")
        table.setHorizontalHeaderLabels(columns)
        
        
        for i in range(l):
            for j in range(n):
                item = QTableWidgetItem(tableData[i][j])
                table.setItem(i,j,item)
        
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
        
        
        completeLayout = QVBoxLayout()
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(table)
        tabLayout.addWidget(addButton)
        
        completeLayout.addWidget(tableName)
        completeLayout.addLayout(tabLayout)
        self.mainLayout.addLayout(completeLayout)
        
        
    def addFieldTableData(self, tableNameColumns, path, name, tableData):
        
            
        def addLine():
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            
        
        addButton = QPushButton("+")
        addButton.clicked.connect(addLine)
        
        tableName = QLabel(name)
        
        table = QTableWidget()
        table.setObjectName(path + " el")
        
        n = len(tableNameColumns)
        l = len(tableData)
        table.setRowCount(l)
        table.setColumnCount(n)
        columns = []
        for i in range(n) :
            typeColumns = tableNameColumns[i][1][0]
            if len(tableNameColumns[i][1]) > 1 :
                for j in range(1, len(tableNameColumns[i][1])):
                    typeColumns += " " + tableNameColumns[i][1][j]
            columns.append(tableNameColumns[i][0]+ "\n(" + typeColumns +")")
        table.setHorizontalHeaderLabels(columns)
        
        
        for i in range(l):
            for j in range(n):
                data = tableData[i][j][0]
                if len(tableData[i][j]) > 0 :
                    for k in range(1, len(tableData[i][j])):
                        data += " " + tableData[i][j][k]
                item = QTableWidgetItem(data)
                table.setItem(i,j,item)
        
        completeLayout = QVBoxLayout()
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(table)
        tabLayout.addWidget(addButton)
        
        completeLayout.addWidget(tableName)
        completeLayout.addLayout(tabLayout)
        self.mainLayout.addLayout(completeLayout)
    
    
    def extraireDonneesEtTypes(self): 
        """parcourt les diff widget de l'espace, on stock dans un dico le nom le widget et le type, retrouve tt les widget enfant de type QCheckBox"""
        self.donnees_et_types = {}
        for edit in self.findChildren(QLineEdit):
            infos = edit.objectName().split()
            if infos[0] in self.donnees_et_types :
                self.donnees_et_types[infos[0]] = ( self.donnees_et_types[infos[0]][0]+ " " + edit.text(),  self.donnees_et_types[infos[0]][1] + " " + infos[1])
            else :
                self.donnees_et_types[infos[0]] = (edit.text(), infos[1])
    
        for combobox in self.findChildren(QComboBox):
            infos = combobox.objectName().split()
            self.donnees_et_types[infos[0]] = (combobox.currentText(), infos[1])

        
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
                else :
                    headers.append(header[1:-1])
            table.append(headers)
                
            for row in range(tablewidget.rowCount()):
                data = []
                for col in range(tablewidget.columnCount()):
                    it = tablewidget.item(row, col)
                    text = it.text() if it is not None else ""
                    data.append(text)
                table.append(data)
            self.donnees_et_types[tablewidget.objectName().split()[0]] = (table, 'el')
    
        print(self.donnees_et_types)
        self.getDataAsField()
        
        
    def getDataAsField(self): 
        self.dataAsField = []
        
        for path in self.donnees_et_types :
            if self.donnees_et_types[path][1] == "el" :
                table = self.donnees_et_types[path][0]
                if type(table[0][0]) == tuple :
                    col = len(table[0])
                    row = len(table)
                    for i in range(1,row):
                        
                        for j in range(0,col):
                            typef = table[0][j][1]
                            name = table[0][j][0]
                            value = [table[i][j]]
                            field = Field(name, typef, path, value )
                            self.dataAsField.append(field)
                            print(field)
                    
                    
                else :
                    col = len(table[0])
                    typesTable = [table[0][0]]
                    if col > 1 :
                        for i in range(1, col):
                            typesTable.append(table[0][i])
                    row = len(table)
                    for i in range(1,row):
                        value = [table[i][0]]
                        for j in range(1,col):
                            value.append(table[i][j])
                        field = Field(path.split("/")[-1],typesTable, path, value )
                        self.dataAsField.append(field)
                            
            else :
                field = Field(path.split("/")[-1],self.donnees_et_types[path][1].split(), path, self.donnees_et_types[path][0].split() )
                self.dataAsField.append(field)
                # print(field.name, field.type, field.path, field.value)
        
        
    # def setDataInField(self):
    #     list_t, list_d, a, b = self.data_xml_structure.strat.iterate(self.specification_xml_structure, self.data_xml_structure)
        
        
    #     for data in list_d:
    #         for field in self.fields:
    #             if data[0] == ('Root' + field.path): #ATTENTION ROOT!!!
    #                 if "el" in data[0]:
    #                     if field.value == ['']:
    #                         field.value = data[1]
    #                     else:
    #                         i = self.fields.index(field)
    #                         new_field = Field(field.name, field.type, field.path, data[1])
    #                         self.fields.insert(i+1, new_field)
                            
    #                 else:
    #                     if isinstance(data[1],list):
    #                         field.value = data[1]
    #                     else:
    #                         field.value = [data[1]]
        

if __name__ == "__main__":
    
    # # Test your XML class
    # xmlStrat = XmlManager()
    # xml = DataType(xmlStrat,"example/FullSpecif.xml")
    # Dataxml = DataType( xmlStrat,"example/Data_FullSpecif.xml")
    # xml.readFile()
    # Dataxml.readFile()
    
    # # for el in Dataxml.content.iter() :
    # #     print(el.getroottree().getpath(el))
    # data_empty = xml.createData()
    # # data_empty.convert2File()

    # field_list = xml.convert2Field(data_empty.content)

    
    
    
    # field1 = Field("Number", ["int"], ".../Number","")
    # field2 = Field("Id", ["int"], ".../Id","")
    # field3 = Field("Name", ["string", "string"],".../Name","")
    # field4 = Field("Number", ["int"], "haha/el/Number","")
    # field5 = Field("Id", ["int"], "haha/el/Id","")
    # field6 = Field("Name", ["string"], "haha/el/Name","")
    # field8 = Field("Number", ["int"], "héhé/el/Number","")
    # field9 = Field("Id", ["int"], "héhé/el/Id","")
    # field10 = Field("Arg", ["string"],".../Arg","")
    # field11 = Field("AAAARRRRGG", ["Float","Float"],"hoho/el","")
    # field12 = Field("Truc", ["string", "enum_SysCoGeo"],".../Truc","")
    
    # field7 = Field("SystemeDeCoordonnées", ["enum_SysCoGeo"], "num/nim/SystemeDeCoordonnées","")
    # fields= [field1, field2,field3, field7, field4, field5, field6, field8, field9, field10, field12, field11]
    
    app = QApplication(sys.argv)
    gui = XmlEditorGUI()
    gui.show()
    sys.exit(app.exec_())