import lxml.etree as etree
from Strategy import Strategy

class XmlManager(Strategy):
    
    def __init__(self, filename):
        self.filename = filename
        self.tree = None
    
    def readFile(self):
        self.tree = etree.parse(self.filename)
        return self.tree
    
    def convert2Xml(self):
        self.tree.write(self.filename,encoding="utf-8", xml_declaration=True)
    