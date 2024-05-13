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
        """
        Function that convert the content into a XML file based on the filename.

        Returns
        -------
        None.

        """
        self.strat.convert2File(self.content,self.filename)
        
    def createData(self) :
        """
        Function that create the DataType 'data' associated with the specifications.
        The content is a tree with the same strucutre as the specification tree but with empty leaves.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
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
    
    def convert2Field(self, dataTree) :
        """
        

        Parameters
        ----------
        dataTree (etree): tree of data, with the same structure that specTree with empty leaves or not
        
        Returns
        -------
        (List of Fields): List of Field who represent each leaf of the data tree, with the type noted in the specifications tree.

        """
        return self.strat.convert2Field(self.content, dataTree)
    
    def updateData(self, fieldList) :
        """
        Fonction that use the mofications wrote by the user, saved on the field list, to update the content of the data tree.
        It set the content of the object DataType 'data'.

        Parameters
        ----------
        field_list (list of Field): List of Field at the output of the GUI, who represent each leaf of the data tree, or new leaves in the case of <el> element

        Returns
        -------
        None.

        """
        self.content = self.strat.updateData(self.content, fieldList)

