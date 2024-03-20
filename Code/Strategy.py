from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def readFile(self):
        pass
    
    @abstractmethod
    def modif(self):
        pass
    
    @abstractmethod
    def convert(self):
        pass
    
    @abstractmethod
    def verif(self):
        pass
    
    @abstractmethod
    def comparer(self):
        pass