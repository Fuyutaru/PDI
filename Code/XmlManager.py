import lxml.etree as etree
import xml.etree.ElementTree as ET
from Strategy import Strategy
import re
from Field import Field
import copy
from DataType import DataType
from dico import Dico
from collections import OrderedDict
from Enumeration import enum

class XmlManager(Strategy):
    
    def __init__(self):
        pass
    
    def readFile(self, filename):
        tree = etree.parse(filename)
        return tree
    
    def verif(self, tree):
        root = tree.getroot()
        version_elem = root.find('Version')
        data_elem = root.find('Data')
        type_elem = root.find('Type')

        # Check if all required elements are present
        if version_elem is None or data_elem is None or type_elem is None:
            return False
        
        # Check version format
        version_format = re.compile(r'"(\d+(\.\d+){2})"')
        version = version_elem.text.strip()
        if not version_format.match(version):
            return False
        
        # Check type
        if type_elem.text.strip() != '"MMVII_Serialization"':
            return False
        
        # All verifications passed
        return True
    
    def convert2File(self, tree, filename):
        tree.write(filename, encoding="utf-8", xml_declaration=True, method="xml")
        
    def convert2Field (self, specTree, dataTree) :
        # Liste pour stocker les objets créés
        field_list = []
        
        root_spec_element = specTree.find('Data')
        
        # Parcours de l'arbre XML en sautant les premières lignes
        for specElement in root_spec_element.iter():
            
            # Test pour sauter les commentaires
            if isinstance(specElement.tag, str) :
                
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
                                obj_value = [val for val in dataElement.text.split(" ")]
                            
                            field = Field(obj_name, obj_type, obj_path, obj_value)
                            field_list.append(field)
                        
                elif len(specElement) != 0 and specElement.tag == "el" :
                    
                    # Récupérer les types associés aux enfants de specElement
                    types = {child.tag: child.text for child in specElement}
                    obj_path = specElement.getroottree().getpath(specElement)[1:]
                    
                    # Parcourir les éléments correspondants dans le fichier de données
                    for elElement in dataTree.findall(obj_path[5:]):
                        
                        if isinstance(elElement.tag, str) :
                            
                            for child in elElement:
                                if isinstance(child.tag, str) :
                                    obj_name = child.tag
                                    obj_path = elElement.getroottree().getpath(child)[1:]
                                    if dataElement.text == None :
                                        obj_value = None
                                    else :
                                        obj_value = [val for val in dataElement.text.split(" ")]
                                    obj_type = [Type for Type in types[obj_name].split(" ")]
                                    
                                    field = Field(obj_name, obj_type, obj_path, obj_value)
                                    field_list.append(field)
                    
        return field_list
        
        
    def createData(self, tree, filename) :
        
        data_tree = copy.deepcopy(tree)
        root_data_element = data_tree.find('Data')
        if root_data_element is not None:
            for element in root_data_element.iter():
                element.text = ''
        else :
            print("Error: Root not find")
            
        data_filename = filename[:-4] + "_data.xml"
        data_XML = DataType(self,data_filename)
        data_XML.content = data_tree
        return data_XML
        
        
    
    def get_node_path(self, node):
        path = []
        while node is not None:
            if isinstance(node.tag, str):
                # print(node.tag)
                path.insert(0, node.tag)  # Insert the tag at the beginning of the path list
            node = node.getparent()
        # print(path)
        return '/'.join(path)
    
    def convert_to_appropriate_type(self, value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value.strip('"')
            
    
    def testCompare(self, datatype, data):
        elt2 = datatype
        elt1 = data

        if (elt2 == "boolean"):
            # print("boooooooooooooooooooooooooooooooool")
            if not (elt1 in ('0', '1', 'True', 'False')):
                # print(elt1)
                print("boooooooooooooooooooooooooooooooool")
                print(elt1)
                return False
        elif (elt2 in enum.enumName):
            # print("j'suis un enuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuum")
            value = enum.enumDict.get(elt2)
            # print(value)
            # print(elt2)
            if elt1 not in value:
                print("enuuuuuuuuuuuuuuuuuuuuuuuum")
                print(elt1)
                return False
        else:
            converted_val = self.convert_to_appropriate_type(elt1)
            # print("type", elt2)
            # print("val", type(elt1))
            # if type(elt1) != elt2:
            #     return False
            if (elt2 == float):
                if (type(converted_val) not in [float, int]):
                    print("floaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaat")
                    print(elt2)
                    print(type(converted_val), converted_val, type(converted_val) not in [float, int])
                    return False
            else:
                if (type(converted_val) != elt2):
                    # print("adfdsfdfdqfsdqfdsqfsdfsqfsf")
                    # print(converted_val)
                    # print(elt2)
                    #pb quand c'est 0 ca compte comme int et non float 
                    print("normalllllllllllllllllllllllllllllllllll")
                    print(converted_val, type(converted_val))
                    print(elt2)
                    return False
            
    
    
    
    def compare(self, type_data, data):
        # type_elements = OrderedDict((element.tag, element_type) for element in r.iter() for element_type in [Dico.content.get(element.text, str)])
        # type_elements = OrderedDict()

        list_t, list_d, paths_t, paths_d = self.iterate(type_data, data)
        
        
        if paths_d != paths_t:
            return False


        print("dsfqs", list_d)
        # print(list_t)
        
        for d in list_d:
            # print(d)
            for t in list_t:
                # print(t)
                if d[0] == t[0]:
                    # print("meme cheminnnnnnnnnnnnnnnnnnnnnnnnnnnn")
                    if d[1] != '':
                    
                        if isinstance(t[1], list) and isinstance(d[1], list):
                            # print("j'suis une listeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                            # print(t[1], "sfhijsqhofhdsfsqifhqifhdsqjfsqijsdfqjs")
                            if len(t[1]) != len(d[1]):
                                return False
                            
                            
                            # on parcours les listes dans le cas où on a plusieurs type de suite
                            for elt1, elt2 in zip(d[1], t[1]):
                                # print("j'suis dans le zippppppppppppppppppp")

                                if (self.testCompare(elt2, elt1) == False):
                                    return False
                        
                        elif (isinstance(t[1], list) and not isinstance(d[1], list)) or (not isinstance(t[1], list) and isinstance(d[1], list)):
                            return False

                        elif (not isinstance(t[1], list) and not isinstance(d[1], list)):
                            #l'autre cas
                            print("casssssssssssssssssssssssssssssss normal")
                            print("type",t[1])
                            print("val", d[1])
                            elt1 = d[1]
                            elt2 = t[1]
                            if (self.testCompare(elt2, elt1) == False):
                                    return False
                    
        print("Truuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuue")
        return True
            
        # return type_elements
    
    def iterate(self, type, data):
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

