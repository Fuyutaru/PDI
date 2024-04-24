from Datatype import Datatype
from lxml import etree
from Champ import Champ
from XmlManager import XmlManager
import os

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
    