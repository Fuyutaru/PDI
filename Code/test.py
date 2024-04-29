from XML import XML
from lxml import etree
from Champ import Champ
from XmlManager import XmlManager

def iterate_xml_elements(root, champs, path=None):
    if path is None:
        path = []
        
    print(f"Called with path: {path}")
    
    for element in root:
        current_path = path + [element.tag]
        if len(element) > 0:
            iterate_xml_elements(element, champs, current_path)
        else:
            nom = element.tag
            type = element.text
            balise = '/'.join(current_path)
            print(f"Leaf Node: {balise} - Type: {type}")
            champs.append(Champ(nom, type, balise))



if __name__ == "__main__":
    # Test your XML class
    xmlStrat = XmlManager("./example/FullSpecif.xml")
    xml = XML("specification")
    xml.readFile(xmlStrat)
    xpath_expression = "./Data/FullSpecifTarget/BitEncoding/Specifs/Type"
    root = xml.content.getroot()
    r = root.xpath("./Data")
    el = root.xpath(xpath_expression)
    el[0].text = "toto"
    # for element in elements:
    #     print("1")
    
    champs = []
    iterate_xml_elements(r, champs)file:///C:/Users/Laurie/Documents/GitHub/PDI/Code/Test_essai.py
    for el in champs:
        print(el.nom, el.type, el.balise)
    # print(champs)
   
    