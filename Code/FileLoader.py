# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:08:21 2024

@author: Laurie
"""


from PyQt5.QtCore import QThread, pyqtSignal


class FileLoader(QThread):
    fileLoaded = pyqtSignal(str)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        with open(self.filename, 'r') as file:
            data = file.read()
            self.fileLoaded.emit(data)