from Datatype import Datatype
from lxml import etree
from Champ import Champ
from XmlManager import XmlManager
import os
import Enumeration

def convert_to_appropriate_type(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value.strip('"')

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    rpath = "example/FullSpecif.xml"
    dpath = "example/Data_FullSpecif.xml"
    path = os.path.join(current_directory, rpath)
    data_path = os.path.join(current_directory, dpath)
    
    xmlStrat = XmlManager()
    dataStrat = XmlManager()
    
    
    specif = Datatype(xmlStrat, path)
    data = Datatype(dataStrat, data_path)
    
    specif.readFile()
    data.readFile()
    
    xpath_expression = "./Data"
    root = specif.content.getroot()
    # r = root.xpath("./Data")
    el = root.xpath(xpath_expression)
    # el[0].text = "toto"
    # print(el[0].text)
    
    # print(specif.verif())
    
    spe = xmlStrat.comparer(specif,data)
    print(spe)
    
    # l = [Enumeration, "CERN", 'enum_TypeCodedTarget']
    # if 'enum_TypeCodedTarget' in Enumeration.enum.enumName:
    #     print("conoooooooooo")
    
    # val = Enumeration.enum.enumDict.get('enum_TypeCodedTarget')
    # if "CERN" in val:
    #     print("haahahhaahahahaah")
    
    # a = [float]
    # b = ['Root/Data/FullSpecifTarget/BitEncoding/Specifs/hihi', '1']
    # if type(b[1]) != a[0]:
    #     print(type(b[1]))
    #     print("connnnnnn")
    tab = ['"1"', '2.2', '4', "flaa"]
    for i in range(len(tab)):
        tab[i] = convert_to_appropriate_type(tab[i])
    print(tab)
    for ele in tab:
        print(type(ele))
    
    
    