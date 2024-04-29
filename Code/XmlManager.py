import lxml.etree as etree
import xml.etree.ElementTree as ET
from Strategy import Strategy
import re
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
    
    
    def comparer(self, type_data, data):
        # type_elements = OrderedDict((element.tag, element_type) for element in r.iter() for element_type in [Dico.content.get(element.text, str)])
        # type_elements = OrderedDict()

        list_t, list_d = self.iterate(type_data, data)


        print("dsfqs", list_d)
        # print(list_t)
        
        for d in list_d:
            # print(d)
            for t in list_t:
                # print(t)
                if d[0] == t[0]:
                    # print("meme cheminnnnnnnnnnnnnnnnnnnnnnnnnnnn")
                    if isinstance(t[1], list) and isinstance(d[1], list) and len(t[1]) == len(d[1]):
                        # print("j'suis une listeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                        # print(t[1], "sfhijsqhofhdsfsqifhqifhdsqjfsqijsdfqjs")
                        # on parcours les listes dans le cas où on a plusieurs type de suite
                        for elt1, elt2 in zip(d[1], t[1]):
                            # print("j'suis dans le zippppppppppppppppppp")

                            if (elt2 == "boolean"):
                                print("boooooooooooooooooooooooooooooooool")
                                if not (elt1 in ('0', '1', 'True', 'False')):
                                    print(elt1)
                                    return False
                            elif (elt2 in enum.enumName):
                                print("j'suis un enuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuum")
                                value = enum.enumDict.get(elt2)
                                print(value)
                                print(elt2)
                                if elt1 not in value:
                                    return False
                            elif elt2 == '':
                                pass
                            else:
                                converted_val = self.convert_to_appropriate_type(elt1)
                                # print("type", elt2)
                                # print("val", type(elt1))
                                # if type(elt1) != elt2:
                                #     return False
                                if (type(converted_val) != elt2):
                                    print("adfdsfdfdqfsdqfdsqfsdfsqfsf")
                                    print(converted_val)
                                    print(elt2)
                                    #pb quand c'est 0 ca compte comme int et non float 
                                    return False
                    else:
                        #l'autre cas
                        pass
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
        
        for element1 in r_t.iter():
            if len(element1) == 0 and isinstance(element1.tag, str):
                path = self.get_node_path(element1)
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
                
                if element2.text is None:
                    text_d = ''
                elif ' ' in element2.text:
                    text_d = element2.text.split()
                        
                else:
                    text_d = element2.text
                
                list_d.append([path_d, text_d])
        
        return list_t, list_d

