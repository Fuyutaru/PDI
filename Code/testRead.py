from XML import XML
from lxml import etree
from Champ import Champ
from XmlManager import XmlManager
import os

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    rpath = "example/FullSpecif.xml"
    path = os.path.join(current_directory, rpath)
    xmlStrat = XmlManager()
    xml = XML("specification", xmlStrat, path)
    xml.readFile()
    xpath_expression = "./Data/FullSpecifTarget/BitEncoding/Specifs/Type"
    root = xml.content.getroot()
    r = root.xpath("./Data")
    el = root.xpath(xpath_expression)
    el[0].text = "toto"
    print(el[0].text)
    
    print(xml.verif())
    
    spe = xmlStrat.comparer(xml.content,el)
    print(spe)
    