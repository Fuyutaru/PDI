import lxml.etree as etree
from Strategy import Strategy
import re
from Field import Field
import copy
from DataType import DataType
from dico import Dico
from Enumeration import enum
import os.path

class XmlManager(Strategy):
    
    def __init__(self):
        pass
    
    def readFile(self, filename):
        """
        Function used to create an ElementTree from the path of the XML file.

        Args:
            filename (str): path of the XML file

        Returns:
            etree: tree generated from the XML file
        """
        tree = etree.parse(filename)
        return tree
    
    def verif(self, tree):
        """
        Function used to verify that the XML file header is correct.

        Args:
            tree (etree): tree that needs to be verified

        Returns:
            _bool_: True if correct | False if incorrect
        """
        root = tree.getroot()
        version_elem = root.find('Version')
        data_elem = root.find('Data')
        type_elem = root.find('Type')

        # Check if all required elements are present
        if version_elem is None or data_elem is None or type_elem is None:
            return False
        
        version_format = re.compile(r'"(\d+(\.\d+){2})"')
        version = version_elem.text.strip()
        if not version_format.match(version):
            return False

        if type_elem.text.strip() != '"MMVII_Serialization"':
            return False
        
        return True
    
    def convert2File(self, tree, filename):
        tree.write(filename, encoding="utf-8", xml_declaration=True, method="xml")
        
    
        
    def createData(self, tree, filename) :
        
        data_tree = copy.deepcopy(tree)
        root_data_element = data_tree.find('Data')
        if root_data_element is not None:
            for element in root_data_element.iter():
                element.text = ''
        else :
            print("Error: Root not find")
            
        data_filename = filename[:-4] + "_data.xml"
        data_XML = DataType(self, data_filename)
        data_XML.content = data_tree
        return data_XML
        
        
    
    def get_node_path(self, node):
        """
        Function used to get the path of a node in an etree.

        Args:
            node (etree): node of the etree

        Returns:
            str: path of the node
        """
        path = []
        while node is not None:
            if isinstance(node.tag, str):
                path.insert(0, node.tag)
            node = node.getparent()
        return '/'.join(path)
    
    def convert_to_appropriate_type(self, value):
        """
        Function used to convert the type of the element in a string to
        its appropriate type.

        Args:
            value (str): the string that will be converted

        Returns:
            any: the real type of the element in the string
        """
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value.strip('"')
            
    
    def testCompare(self, datatype, data):
        """
        Function used to compare data against a given data type.

        Args:
            datatype (str or type): The data type against which data will be compared.
            data (str or int or float or bool): The data to be compared.

        Returns:
            bool: True if the data matches the specified data type, False otherwise.
        """
        elt2 = datatype
        elt1 = data

        if (elt2 == "boolean"):
            if not (elt1 in ('0', '1', 'True', 'False')):
                return False
        elif (elt2 in enum.enumName):
            value = enum.enumDict.get(elt2)
            if elt1 not in value:
                return False
        else:
            converted_val = self.convert_to_appropriate_type(elt1)
            if (elt2 == float):
                if (type(converted_val) not in [float, int]):
                    return False
            else:
                if (type(converted_val) != elt2):
                    return False
            
    
    
    
    def compare(self, type_data, data):
        """
        Compares the structure and content of data against a given data type.

        Args:
            type_data (DataType): the data structure which contains the data of an XML file
            data (DataType): the type structure which contains the specified type of an XML file

        Returns:
            bool: True if the structure and content of data match the specified data type, False otherwise.
        """
        
        list_t, list_d, paths_t, paths_d = self.iterate(type_data, data)
        
        if paths_d != paths_t:
            return False
        
        for d in list_d:
            for t in list_t:
                if d[0] == t[0]:
                    if d[1] != '':
                        if isinstance(t[1], list) and isinstance(d[1], list):
                            if len(t[1]) != len(d[1]):
                                return False
                            
                            # We iterate through the lists in case we have multiple types in a row.
                            for elt1, elt2 in zip(d[1], t[1]):
                                if (self.testCompare(elt2, elt1) == False):
                                    return False
                        
                        elif (isinstance(t[1], list) and not isinstance(d[1], list)) or (not isinstance(t[1], list) and isinstance(d[1], list)):
                            return False

                        elif (not isinstance(t[1], list) and not isinstance(d[1], list)):
                            elt1 = d[1]
                            elt2 = t[1]
                            if (self.testCompare(elt2, elt1) == False):
                                    return False
                    
        return True

    
    def iterate(self, type, data):
        """
        Function that iterates over the structure of the data type and the data content, extracting paths and values.

        Args:
            type (DataType): the data structure which contains the data of an XML file
            data (DataType): the type structure which contains the specified type of an XML file

        Returns:
            tuple: A tuple containing four lists:
                - list_t (list): A list of tuples representing the structure of the data type. Each tuple contains the path of the data and its type.
                - list_d (list): A list of tuples representing the content of the data. Each tuple contains the path of the data and its value.
                - paths_t (list): A list of paths extracted from the structure of the data type.
                - paths_d (list): A list of paths extracted from the content of the data.
        """
        # Get the root elements of both XML files
        root_t = type.content.getroot()
        root_d = data.content.getroot()
        
        r_t = root_t.find('Data')
        r_d = root_d.find('Data')    

        list_t = []
        list_d = []
        
        paths_t = []
        paths_d = []
        
        for element1 in r_t.iter():
            if len(element1) == 0 and isinstance(element1.tag, str):
                path = self.get_node_path(element1)
                if path not in paths_t:
                    paths_t.append(path)
                if ' ' in element1.text:
                    text = element1.text.split()
                    for i in range(len(text)):
                        text[i] = Dico.content.get(text[i], str)
                else:
                    text = Dico.content.get(element1.text, str)
                
                list_t.append([path, text])
        
        for element2 in r_d.iter():
            if len(list(element2)) == 0 and isinstance(element2.tag, str):
                path_d = self.get_node_path(element2)
                if path_d not in paths_d:
                    paths_d.append(path_d)
                
                if element2.text is None:
                    text_d = ''
                elif ' ' in element2.text:
                    text_d = element2.text.split()
                        
                else:
                    text_d = element2.text
                
                list_d.append([path_d, text_d])
        
        return list_t, list_d, paths_t, paths_d


    def convert2Field (self, specTree, dataTree) :
        # Liste pour stocker les objets créés
        field_list = []
        
        root_spec_element = specTree.find('Data')
        
        NbrChild = 0
        NbrPass = 0
        # Parcours de l'arbre XML en sautant les premières lignes
        for specElement in root_spec_element.iter():
            
            # Test pour sauter les commentaires
            if isinstance(specElement.tag, str) :
                
                if NbrChild > NbrPass :
                    NbrPass += 1
                    
                else :
                    # Création d'un objet pour chaque balise à la fin de branche
                    if len(specElement) == 0 and specElement.tag != "el":  # Vérifier si c'est une balise finale (pas d'enfants)
                        obj_name = specElement.tag
                        obj_type = [Type for Type in specElement.text.split(" ")]
                        obj_path = specElement.getroottree().getpath(specElement)[1:]
                        
                        dataElement = dataTree.find(obj_path[4:])
                        
                        if dataElement.text == None :
                            obj_value = None
                        else :
                            obj_value = [val for val in dataElement.text.split(" ")]
                        
                        # Créer l'objet et l'ajouter à la liste
                        field = Field(obj_name, obj_type, obj_path, obj_value)
                        field_list.append(field)
                            
                    elif len(specElement) == 0 and specElement.tag == "el" :
                        
                        obj_name = specElement.tag
                        obj_type = [Type for Type in specElement.text.split(" ")]
                        obj_path = specElement.getroottree().getpath(specElement)[1:]
                        
                        for elElement in dataTree.findall(obj_path[4:]):
                            if isinstance(elElement.tag, str) :
                                if dataElement.text == None :
                                    obj_value = None
                                else :
                                    obj_value = [val for val in elElement.text.split(" ")]
                                
                                field = Field(obj_name, obj_type, obj_path, obj_value)
                                field_list.append(field)
                            
                    elif len(specElement) != 0 and specElement.tag == "el" :
                
                        # Récupérer les types associés aux enfants de specElement
                        types = {child.tag: child.text for child in specElement}
                        el_path = specElement.getroottree().getpath(specElement)
                        
                        # Parcourir les éléments correspondants dans le fichier de données
                        for elElement in dataTree.findall(el_path[5:]):
                            
                            if isinstance(elElement.tag, str) :
                                
                                NbrChild = 0
                                for child in elElement:
                                    NbrChild += 1
                                    if isinstance(child.tag, str) :
                                        obj_name = child.tag
                                        obj_path = child.getroottree().getpath(child)[1:]
                                        
                                        if '[' in obj_path :
                                            obj_path = obj_path.split('[')[0] + obj_path.split(']')[1]
                                            
                                        if child.text == None :
                                            obj_value = None
                                        else :
                                            obj_value = [val for val in child.text.split(" ")]
                                        obj_type = [Type for Type in types[obj_name].split(" ")]
                                        
                                        field = Field(obj_name, obj_type, obj_path, obj_value)
                                        field_list.append(field)
                    
                 
        return field_list
        
    
    def updateData (self, dataTree, fieldList) :
       
        # Création du dictionnaire associant chaque chemin à une liste d'indices
        path_to_indices = {}
        
        # Parcourir les objets Field et remplir le dictionnaire
        for index, field in enumerate(fieldList):
            path = field.path
            if path not in path_to_indices:
                path_to_indices[path] = []  # Initialiser la liste vide pour ce chemin
            path_to_indices[path].append(index)  # Ajouter l'indice à la liste correspondante

        for obj_path in path_to_indices :
            field0 = fieldList[path_to_indices[obj_path][0]]
    
            if field0.name != 'el' and obj_path[:-len(field0.name)][-4:] != '/el/' :
                
                new_value = field0._value
                new_text = ''
                if new_value != None :
                    for value in new_value :
                        new_text = new_text + value + " "
                    new_text = new_text[:-1]
                
                dataTree.find(obj_path[4:]).text = new_text
                
            elif field0.name == 'el' :
                
                elList = path_to_indices[obj_path]
                elData = dataTree.findall(obj_path[4:])
                NumberLeaves = len(elData)
                i = 0
                
                for el in elData :
                    if isinstance(el.tag, str) :
                        new_value = fieldList[elList[i]]._value
                        new_text = ''
                        if new_value != None :
                            for value in new_value :
                                new_text = new_text + value + " "
                            new_text = new_text[:-1]
                        
                        el.text = new_text
                        i += 1
                
                
                if len(elList) > NumberLeaves :
                    
                    existing_element = elData[-1]
                    j = NumberLeaves
                    for el in elList[NumberLeaves:] :
                        new_leaf = etree.Element(existing_element.tag, attrib=existing_element.attrib)
                        
                        new_value = fieldList[elList[j]]._value
                        new_text = ''
                        if new_value != None :
                            for value in new_value :
                                new_text = new_text + value + " "
                            new_text = new_text[:-1]
                            
                        new_leaf.text = new_text
                        j+=1
                        
                        parent_element = existing_element.getparent()
                        parent_element.append(new_leaf)
            
            else :
                parent_path, childName = obj_path.split('/el/')
                
                childData = dataTree.findall(obj_path[4:])
                
                childList = path_to_indices[obj_path]
                
                i = 0
                for child in childData :
                    if isinstance(child.tag, str) :
                        
                        if child.tag == childName :
                            new_value = fieldList[childList[i]]._value
                            new_text = ''
                            if new_value != None :
                                for value in new_value :
                                    new_text = new_text + value + " "
                                new_text = new_text[:-1]
                            
                            child.text = new_text
                            i += 1
                
                if len(childList) > i :
                    existing_parent = childData[0].getparent()
                    
                    j = i
                    for child in childList[j:] :
                        new_branch = etree.Element(existing_parent.tag, attrib=existing_parent.attrib)
                        for leaf in existing_parent :
                            if isinstance(leaf.tag, str) :
                                new_leaf = etree.Element(leaf.tag, attrib=leaf.attrib)
                                if new_leaf.tag == childName :
                                    new_value = fieldList[childList[j]]._value
                                    new_text = ''
                                    if new_value != None :
                                        for value in new_value :
                                            new_text = new_text + value + " "
                                        new_text = new_text[:-1]
                                    new_leaf.text = new_text
                                new_branch.append(new_leaf)
  
                        j+=1
                        parent_branch = existing_parent.getparent()
                        parent_branch.append(new_branch)
                    
        return dataTree      