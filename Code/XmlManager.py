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
        
    def convert2Field (self, specTree, dataTree) :
        # Liste pour stocker les objets créés
        field_list = []
        
        root_spec_element = specTree.find('Data')
        
        # Parcours de l'arbre XML en sautant les premières lignes
        for specElement in root_spec_element.iter():
            
            # Test pour sauter les commentaires
            if isinstance(specElement.tag, str) :
                
                # Création d'un objet pour chaque balise à la fin de branche
                if len(specElement) == 0 and specElement.name != "el":  # Vérifier si c'est une balise finale (pas d'enfants)
                    obj_name = specElement.tag
                    obj_type = [Type for Type in specElement.text.slice("/")]
                    obj_path = specElement.getroottree().getpath(specElement)
                    
                    dataElement = specTree.find(obj_path)
                    
                    obj_value = [val for val in dataElement.text.slice(" ")]
                    
                    # Créer l'objet et l'ajouter à la liste
                    field = Field(obj_name, obj_type, obj_path, obj_value)
                    field_list.append(field)
                        
                elif len(specElement) == 0 and specElement.name == "el" :
                    
                    obj_name = specElement.tag
                    obj_type = [Type for Type in specElement.text.slice("/")]
                    obj_path = specElement.getroottree().getpath(specElement)
                    
                    for elElement in dataTree.findall(obj_path):
                        if isinstance(specElement.tag, str) :
                            obj_value = elElement.text
                            
                            field = Field(obj_name, obj_type, obj_path, obj_value)
                            field_list.append(field)
                        
                elif len(specElement) != 0 and specElement.name == "el" :
                    
                    # Récupérer les types associés aux enfants de specElement
                    types = {child.tag: child.text for child in specElement}
                    # PROBLEME PARCE QUE SI TYPE = DOUBLE DOUBLE, DICO = PAS CONTENT
                    # Parcourir les éléments correspondants dans le fichier de données
                    for elElement in dataTree.findall(obj_path):
                        if isinstance(specElement.tag, str) :
                            
                            for child in elElement:
                                if isinstance(specElement.tag, str) :
                                    obj_name = child.tag
                                    obj_path = elElement.getroottree().getpath(elElement)
                                    obj_value = child.text
                                    obj_type = types[obj_name]
                                    
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
        data_XML = DataType("data",self,data_filename)
        data_XML.content = data_tree
        return data_XML
        
        
    
