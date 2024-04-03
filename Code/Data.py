from abc import ABC, abstractmethod

class Data(ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def readFile(self):
        pass
  
    