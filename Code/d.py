
class DataType():
    
    def __init__(self, strat, filename):
        self.content = None
        self.strat = strat
        self.filename = filename
        
    def readFile(self):
        """
        Reads the content of the file using the specified strategy and stores it in the `content` attribute.

        Returns:
            None
        """
        self.content = self.strat.readFile(self.filename)
    
    def convert2File(self):
        self.strat.convert2File(self.content,self.filename)
        
    def convert2Field(self, dataTree) :
        return self.strat.convert2Field(self.content, dataTree)
        
    def createData(self) :
        return self.strat.createData(self.content, self.filename)
    
    def verif(self):
        """
        Verifies the content using the specified strategy.

        Returns:
            bool: True if the content is valid according to the strategy, False otherwise.
        """
        return self.strat.verif(self.content)
    
    def compare(self, typeTree, dataTree):
        """
        Compares the structure and content of a typeTree with a dataTree using the specified strategy.

        Args:
            typeTree (DataType): The tree representing the type of the data.
            dataTree (DataType): The tree representing the content of the data.

        Returns:
            bool: True if the structure and content of dataTree match the typeTree, False otherwise.
        """
        return self.strat.compare(typeTree, dataTree)

