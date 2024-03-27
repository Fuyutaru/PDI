from XML import XML
from lxml import etree
from Champ import Champ
from XmlManager import XmlManager

if __name__ == "__main__":
    xmlStrat = XmlManager("./example/FullSpecif.xml")
    xml = XML("specification", xmlStrat)
    xml.readFile()
    xpath_expression = "./Data/FullSpecifTarget/BitEncoding/Specifs/Type"
    root = xml.content.getroot()
    r = root.xpath("./Data")
    el = root.xpath(xpath_expression)
    el[0].text = "toto"
    print(el[0].text)
    
    print(xml.verif())
    