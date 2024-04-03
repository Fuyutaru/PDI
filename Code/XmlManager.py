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
    
    
    
    def comparer(self, type, data):
        # Comparaison de structure
        type_elements = OrderedDict((element.tag, element_type) for element in type.iter() for element_type in [Dico.content.get(element.text, str)])
        return type_elements