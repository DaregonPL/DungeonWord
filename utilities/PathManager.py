import json
from os.path import exists


class Paths():
    def __init__(self, pathfile):
        """Meant to manage paths"""
        if exists(pathfile):
            with open(pathfile) as pfile:
                self.paths = json.load(pfile)
        else:
            raise FileNotFoundError(f'\'{pathfile}\' is required for start')

    def check(self):
        self.notfound = []
        for p in self.paths:
            if not exists(self.paths[p]):
                self.notfound.append(f'"{self.paths[p]}"')
        if self.notfound:
            raise FileNotFoundError(', '.join(self.notfound) +
                                    ' are required for start')

    def get(self):
        return self.paths
