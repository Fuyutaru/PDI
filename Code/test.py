from XML import DataType
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
    xmlStrat = XmlManager()
    xml = DataType("specification", xmlStrat,"example/FullSpecif.xml")
    xml.readFile()
    data_xml = xml.createData()
    data_xml.convert2File()
    
    # xpath_expression = "./Data/FullSpecifTarget/BitEncoding/Specifs/Type"
    # root = xml.content.getroot()
    # r = root.xpath("./Data")
    # el = root.xpath(xpath_expression)
    # el[0].text = "toto"
    # # for element in elements:
    # #     print("1")
    
    # champs = []
    # iterate_xml_elements(r, champs)
    # for el in champs:
    #     print(el.nom, el.type, el.balise)
    # # print(champs)

   
    