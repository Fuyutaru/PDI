from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def readFile(self):
        pass
    
    @abstractmethod
    def convert2File(self):
        pass
    
    @abstractmethod
    def createData(self, tree, filename):
        pass
    
    @abstractmethod
    def convert2Field(self, specTree, dataTree):
        pass
    
    @abstractmethod
    def verif(self):
        pass
    
    @abstractmethod
    def compare(self):
        pass
    
    @abstractmethod
    def updateData(self, dataTree, fieldList):
        pass