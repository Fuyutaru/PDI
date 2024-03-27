from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def readFile(self):
        pass
    
    @abstractmethod
    def convert2Xml(self):
        pass
    
    @abstractmethod
    def createData(self):
        pass
    
    # @abstractmethod
    # def verif(self):
    #     pass
    
    # @abstractmethod
    # def comparer(self):
    #     pass