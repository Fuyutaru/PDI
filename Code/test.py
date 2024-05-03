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
    xml = DataType(xmlStrat,"example/FullSpecif.xml")
    Dataxml = DataType(xmlStrat,"example/Data_FullSpecif - Copie.xml")
    xml.readFile()
    Dataxml.readFile()
    
    # for el in Dataxml.content.iter() :
    #     print(el.getroottree().getpath(el))
    data_empty = xml.createData()
    # data_empty.convert2File()

    field_list = xml.convert2Field(Dataxml.content)
    # for i in range (len(field_list)) :
    #     print(field_list[i].name, field_list[i]._value)
    print('############################')
    data_empty.updateData(field_list)
    # Dataxml.convert2File()
    
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

   
