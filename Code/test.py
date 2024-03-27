from XML import XML
from lxml import etree
from Champ import Champ
import os

def iterate_xml_elements(root, path=[], champs=[]):
    for element in root:
        current_path = path + [element.tag]
        if len(element) > 0:
            iterate_xml_elements(element, current_path, champs)
        else:
            nom = element.tag
            type = element.text
            balise = '/'.join(current_path)
            print(f"Leaf Node: {balise} - Type: {type}")
            champs.append(Champ(nom, type, balise))


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    xml_file_path = os.path.join(dir_path, 'example', 'FullSpecif.xml')
    
    # Test your XML class
    tree = etree.parse(xml_file_path)
    xml_instance = XML("xml", tree)
    # print("XML Type:", xml_instance.type)
    # print("XML Content:", xml_instance.content)

    xpath_expression = "./Data/FullSpecifTarget/BitEncoding/Specifs/Type"
    
    root = xml_instance.content.getroot()
    r = root.xpath("./Data")
    # elements = xml_instance.content.find(xpath_expression)
    elements = root.xpath(xpath_expression)
    el = elements
    el[0].text = "toto"
    print(el[0].text)
    print(elements[0].text)
    # for element in elements:
    #     print("1")
    
    champs = []
    iterate_xml_elements(r, champs= champs)
    for el in champs:
        print(el.nom, el.type, el.balise)
    # print(champs)
   
    