import lxml.etree as etree
from Strategy import Strategy

class XmlManager(Strategy):
    
    def __init__(self):
        pass
    
    def readFile(self,filename):
        tree = etree.parse(filename)
        return tree
    
    def convert2Xml(self, tree, filename):
        tree.write(filename, encoding="utf-8", xml_declaration=True, method="xml")
        
    def createData(self, element, depth) :
        
        # i = 0
        # for element in data_tree.iter():
        #     if i > 4 :
        #         element.text = ''
        #     i+=1
        
        max_depth = 3
        
        if depth > max_depth:
            element.text = ''
            # Récupérer l'indentation à partir de l'élément parent s'il a déjà du texte
            parent_text = element.getparent().text
            if parent_text and not parent_text.isspace():
                # Utiliser l'indentation du parent pour les éléments enfants
                indentation = parent_text[:parent_text.index('\n') + 1] if '\n' in parent_text else ''
                for child in element:
                    child.tail = indentation
            else:
                # Sinon, récupérer l'indentation du dernier enfant s'il a du texte
                last_child = element[-1] if len(element) > 0 else None
                last_child_text = last_child.tail if last_child is not None else ''
                if last_child_text and not last_child_text.isspace():
                    indentation = '\n' + ' ' * (len(last_child_text) - len(last_child_text.lstrip()))
                    # Appliquer l'indentation aux éléments enfants
                    for child in element:
                        child.tail = indentation
        for child in element:
            self.createData(child, depth + 1)
    