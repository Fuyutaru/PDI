from DataType import DataType
from lxml import etree
from Field import Field
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
            name = element.tag
            type = element.text
            root = '/'.join(current_path)
            print(f"Leaf Node: {root} - Type: {type}")
            champs.append(Field(name, type, root,0))


if __name__ == "__main__":
    
    
    # Test your XML class
    xmlStrat = XmlManager()
    xml = DataType("specification", xmlStrat,"example/FullSpecif.xml")
    xml.readFile()
    data_xml = xml.createData()
    data_xml.convert2File()
    
    field_list = xml.convert2Field()
    for i in range (5) :
        print(field_list[i].name)
    
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

   
    