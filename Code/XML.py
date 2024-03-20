import lxml.etree as etree
from Data import Data  

class XML(Data):
    
    def __init__(self, type, content):
        super().__init__()  # appel du constructeur de la classe parente
        # initialisation d'autres attributs spécifiques à la classe XML
        self.type = type
        self.content = content
        
        
    # le champ va juste aller chercher le data et l'afficher mais en soit, quand on écrit dans le champ ca ne le
    # change pas en temps réel mais qu'une fois qu'on le sauvegarde.
    
    # def readfile(self, file_path):
    #     with open(file_path, 'rb') as f:
    #         self.content = etree.parse(f)
    #     self.type = "XML"

