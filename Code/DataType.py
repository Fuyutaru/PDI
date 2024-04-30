class DataType ():
    
    def __init__(self, type, strat,filename):
        super().__init__()  # appel du constructeur de la classe parente
        # initialisation d'autres attributs spécifiques à la classe XML
        self.type = type
        self.content = None
        self.strat = strat
        self.filename = filename
        

    def readFile(self):
        self.content = self.strat.readFile(self.filename)
        
    def convert2File(self):
        self.strat.convert2File(self.content,self.filename)
        
    def convert2Field(self, dataTree) :
        return self.strat.convert2Field(self.content, dataTree)
        
    def createData(self) :
        return self.strat.createData(self.content, self.filename)
        

