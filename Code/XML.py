import lxml.etree as etree
from Data import Data  
from Strategy import Strategy

class XML(Data, Strategy):
    
    def __init__(self, type, strat,filename):
        super().__init__()  # appel du constructeur de la classe parente
        # initialisation d'autres attributs spécifiques à la classe XML
        self.type = type
        self.content = None
        self.strat = strat
        self.filename = filename
        

    def readFile(self):
        self.content = self.strat.readFile(self.filename)
        
    def convert2Xml(self):
        self.strat.convert2Xml(self.content,self.filename)
        
    def createData(self) :
        data_tree = self.strat.createData(self.content)
        data_filename = self.filename[:-4] + "_data.xml"
        data_XML = XML("data",self.strat,data_filename)
        data_XML.content = data_tree
        return data_XML
        
        
    # def readfile(self, file_path):
    #     with open(file_path, 'rb') as f:
    #         self.content = etree.parse(f)
    #     self.type = "XML"

