class Field():
    def __init__(self, name, type, path, value):
        self.name = name
        self.type = type
        self.path = path
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if new_value != self._value:
            self._value = new_value