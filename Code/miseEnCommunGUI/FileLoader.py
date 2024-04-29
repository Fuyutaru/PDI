# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:01:50 2024

@author: Svetie
"""

from PyQt5.QtCore import QThread, pyqtSignal

#module pour charger des fichiers en arriere plan

class FileLoader(QThread):
    fileLoaded = pyqtSignal(str)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        try:
            with open(self.filename, 'r') as file:
                data = file.read()
                self.fileLoaded.emit(data)
        except Exception as e:
            print(f"Failed to load file: {str(e)}")
            self.fileLoaded.emit("")