import sys
from PyQt5.QtWidgets import QApplication
from GUI import GUI  
from Champ import Champ  

def main():
    app = QApplication(sys.argv)

    champ1 = Champ("Number", "int", 1)
    champ2 = Champ("Id", "int", 2)
    champ3 = Champ("Name", "string", "Sample Name")
    champs = [champ1, champ2, champ3]

    window = GUI(champs)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



