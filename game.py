from random import randint
import json
from os.path import exists

'''
 ==  P R O J E C T   I N F O  ==
'''

AUTHOR = 'VovLer Games (DaregonPL)'
NAME = 'DungeonWord'
VERSION = '0.1'
inDev = True


class AVGame():
    """DungeonWord game class""" 
    def __init__(self, paths):
        print('|==> GAME INIT <==|')
        self.FP = paths
        with open(self.FP['rules']) as rulesfile:
            self.rules = json.load(rulesfile)
        with open(self.FP['logo']) as logofile:
            self.logo = logofile.read()
        print('ready.')

    def start(self):
        self.menu()

    def menu(self):
        print(f'\n\n{self.logo}\n')
        diffC = Choice([x for x in self.rules], 'Choose the difficulty',
                       cmd=['help', 'back'])


class Choice():
    def __init__(self, options, heading, cmd=None):
        self.binds, self.cmd = {}, cmd
        for x in range(len(options)):
            self.binds[x + 1] = options[x]
        scopes = [f"\"{x}\"" for x in cmd]
        while 1:
            print(f'\n┏━ {heading} ━┫▶')
            [print(f'┃{n}. {val}') for n, val in self.binds.items()]
            print('┃')
            print(f'┣ {", ".join(scopes)} are available') if cmd else 0
            self.ans = input('┗┫')
            if self.ans in self.binds or self.ans in cmd \
                    or self.ans in [y for x, y in self.binds.items()]:
                break


#                           = Getting and checking Paths =
if exists('content/paths.json'):
    with open('content/paths.json') as pathfile:
        FPath = json.load(pathfile)
else:
    raise FileNotFoundError('\'content/paths.json\' is required for start')
notfound = []
for p in FPath:
    notfound.append(f'"{FPath[p]}"') if not exists(FPath[p]) else 0
if notfound:
    raise FileNotFoundError(', '.join(notfound) + ' are required for start')

#                           = Registering build =
with open(FPath['build']) as bld:
    BUILD = int(bld.read()) + 1
if inDev:
    with open(FPath['build'], 'w') as bld:
        bld.write(str(BUILD))
print(f'{NAME} v{VERSION}.{BUILD}\n  by {AUTHOR}')

game = AVGame(FPath)
game.start()
