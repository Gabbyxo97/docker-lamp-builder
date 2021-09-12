import yaml

class YMLFile:
    __path = None
    obj = None

    def __init__(self, path):
        self.__path = path

        with open(path, 'r') as fh:
            self.obj = yaml.load(fh, Loader=yaml.SafeLoader)

    def debug(self):
        print(self.obj)

    def save(self):
        with open(self.__path, 'w') as file:
            yaml.dump(self.obj, file)
