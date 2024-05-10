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
    def convert2Field(self):
        pass
    
    @abstractmethod
    def createData(self):
        pass
    
    @abstractmethod
    def verif(self):
        pass
    
    @abstractmethod
    def compare(self):
        pass
    
    @abstractmethod
    def updateData(self):
        pass