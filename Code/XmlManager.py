import lxml.etree as etree
from Strategy import Strategy
import re

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
    
    def comparer(self, data):
        spec_tree = self.tree

        # Compare versions
        spec_version = spec_tree.find('Version').text.strip()
        data_version = data.find('Version').text.strip()
        if spec_version != data_version:
            return False
        
        # Compare tag structure and order
        spec_tags = [elem.tag for elem in spec_tree.iter()]
        data_tags = [elem.tag for elem in data.iter()]
        if spec_tags != data_tags:
            return False
        
        # Compare data type
        spec_type = spec_tree.find('Data/FullSpecifTarget/BitEncoding/Specifs/Type').text.strip()
        data_type = data.find('Data/FullSpecifTarget/BitEncoding/Specifs/Type').text.strip()
        if spec_type != data_type:
            return False
        
        # All comparisons passed
        return True