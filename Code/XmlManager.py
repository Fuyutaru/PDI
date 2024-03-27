import lxml.etree as etree
from Strategy import Strategy

class XmlManager(Strategy):
    
    def __init__(self, filename):
        self.filename = filename
        self.tree = None
    
    def readFile(self):
        self.tree = etree.parse(self.filename)
        return self.tree
    