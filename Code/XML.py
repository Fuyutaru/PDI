import lxml.etree as etree
from Data import Data  
from Strategy import Strategy

class XML(Data, Strategy):
    
    def __init__(self, type, strat, filename):
        super().__init__()  # appel du constructeur de la classe parente
        # initialisation d'autres attributs spécifiques à la classe XML
        self.type = type
        self.content = None
        self.strat = strat
        self.filename = filename
        
    def readFile(self):
        self.content = self.strat.readFile(self.filename)
    
    def verif(self):
        return self.strat.verif(self.content)

