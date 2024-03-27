import lxml.etree as etree
from Data import Data  
from Strategy import Strategy

class XML(Data, Strategy):
    
    def __init__(self, type):
        super().__init__()  # appel du constructeur de la classe parente
        # initialisation d'autres attributs spécifiques à la classe XML
        self.type = type
        self.content = None
        
    def readFile(self, xmlStrat):
        self.content = xmlStrat.readFile()
    
    # def readfile(self, file_path):
    #     with open(file_path, 'rb') as f:
    #         self.content = etree.parse(f)
    #     self.type = "XML"

