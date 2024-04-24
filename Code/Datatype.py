# import lxml.etree as etree
# from Data import Data  


class Datatype():
    
    def __init__(self, type, strat, filename):
        # super().__init__()  
        self.content = None
        self.strat = strat
        self.filename = filename
        
    def readFile(self):
        self.content = self.strat.readFile(self.filename)
    
    def verif(self):
        return self.strat.verif(self.content)
    
    def comparer(self):
        pass

