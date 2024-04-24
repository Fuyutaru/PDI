import lxml.etree as etree
from Strategy import Strategy
import re
from Field import Field
import copy
from DataType import DataType

class XmlManager(Strategy):
    
    def __init__(self):
        pass
    
    def readFile(self,filename):
        tree = etree.parse(filename)
        return tree
    
    def verif(self):
        root = self.tree.getroot()
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
        
    def convert2Field (self, tree) :
        # Liste pour stocker les objets créés
        field_list = []
        
        root_data_element = tree.find('Data')
        
        # Parcours de l'arbre XML en sautant les premières lignes
        for element in root_data_element.iter():
           
            # Création d'un objet pour chaque balise à la fin de branche
            if len(element) == 0:  # Vérifier si c'est une balise finale (pas d'enfants)
                obj_name = element.tag
                obj_type = None  # Vous devez définir la logique pour déterminer le type
                obj_root = element.getroottree().getpath(element)
                obj_value = element.text
                
                # Créer l'objet et l'ajouter à la liste
                field = Field(obj_name, obj_type, obj_root, obj_value)
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
        data_XML = DataType("data",self,data_filename)
        data_XML.content = data_tree
        return data_XML
        
        
    
