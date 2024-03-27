import lxml.etree as etree
from Strategy import Strategy
import copy

class XmlManager(Strategy):
    
    def __init__(self):
        pass
    
    def readFile(self,filename):
        tree = etree.parse(filename)
        return tree
    
    def convert2Xml(self, tree, filename):
        tree.write(filename, encoding="utf-8", xml_declaration=True, method="xml")
        
    def createData(self, tree) :
        data_tree = copy.deepcopy(tree)
        i = 0
        for element in data_tree.iter():
            if i > 4 :
                element.text = ''
            i+=1
        return data_tree
    