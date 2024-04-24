import lxml.etree as etree
from Strategy import Strategy
import re
from dico import Dico
from collections import OrderedDict

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
            path.insert(0, node.tag)  # Insert the tag at the beginning of the path list
            node = node.getparent()
        return '/'.join(path)
    
    
    def comparer(self, type, data):
        # Comparaison de structure
        root_t = type.content.getroot()
        r_t = root_t.find('Data')
        
        root_d = data.content.getroot()
        r_d = root_d.find('Data')    
        
        # type_elements = OrderedDict((element.tag, element_type) for element in r.iter() for element_type in [Dico.content.get(element.text, str)])
        # type_elements = OrderedDict()

        list_t = []
        list_d = []
        for element1, element2 in zip(r_t.iter(), r_d.iter()):
            
            if len(element1) == 0:
                
                # element_type = Dico.content.get(element1.text, str)
                # print(element1.tag)
                # print(element_type)
                
                path = self.get_node_path(element1)
                # print(path)
                
                if ' ' in element1.text:
                    text = element1.text.split()
                    for i in range(len(text)):
                        # print("aaaaaaaaaaaaaaaa : ", text[i] )
                        text[i] = Dico.content.get(text[i], str)
                    # print(text)
                #     # element_type = Dico.content.get(element1.text, str)
                else:
                    text = Dico.content.get(element1.text, str)
                
                list_t.append([path, text])
                # print("dslkjfgqlqsjfhsif :", list_t)
                # print("tag : ", element1.tag)
                # print(element_type)
                
            if len(element2) == 0:
                path_d = self.get_node_path(element2)
                
                if ' ' in element2.text:
                    text_d = element2.text.split()
                else:
                    text_d = element2.text
                
                list_d.append([path_d, text_d])

        print("dsfqs", list_d)
        
        # return type_elements