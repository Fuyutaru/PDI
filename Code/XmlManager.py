import lxml.etree as etree
from Strategy import Strategy

class XmlManager(Strategy):
    
    def __init__(self):
        pass
    
    def readFile(self,filename):
        tree = etree.parse(filename)
        return tree
    
    def convert2File(self, tree, filename):
        tree.write(filename, encoding="utf-8", xml_declaration=True, method="xml")
    