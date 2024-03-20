import abc
import lxml.etree as etree

class Data(abc.ABC):
    def __init__(self):
        pass
        
    # le content peut être initialiser dans le main en lisant le  fichier
    # avec content = etree.parse("data.xml") par exemple