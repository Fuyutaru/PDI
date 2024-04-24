from Data import Data  
from Strategy import Strategy
import copy


class DataType ():
    
    def __init__(self, type, strat,filename):
        super().__init__()  # appel du constructeur de la classe parente
        # initialisation d'autres attributs spécifiques à la classe XML
        self.type = type
        self.content = None
        self.strat = strat
        self.filename = filename
        

    def readFile(self):
        self.content = self.strat.readFile(self.filename)
        
    def convert2File(self):
        self.strat.convert2File(self.content,self.filename)
        
    def createData(self) :
        
        data_tree = copy.deepcopy(self.content)
        root_data_element = data_tree.find('Data')
        if root_data_element is not None:
            for element in root_data_element.iter():
                element.text = ''
        else :
            print("Error: Root not find")
            
        data_filename = self.filename[:-4] + "_data.xml"
        data_XML = DataType("data",self.strat,data_filename)
        data_XML.content = data_tree
        return data_XML
        

