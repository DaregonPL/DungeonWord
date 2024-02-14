import json
from random import randint
from os.path import exists
from base64 import b64encode
from utilities.Choice import Choice
from utilities.PathManager import Paths
from utilities.Help import Help

'''
 ==  P R O J E C T   I N F O  ==
'''

AUTHOR = 'VovLer Games (DaregonPL)'
NAME = 'DungeonWord'
VERSION = '0.1'
inDev = True


class AVGame():
    """DungeonWord game class""" 
    def __init__(self, paths, PI):
        print('|==> GAME INIT <==|')
        self.FP = paths
        self.PI = {'A': PI[0], 'N': PI[1], 'V': PI[2], 'B': PI[3]}
        with open(self.FP['rules']) as rulesfile:
            self.rules = json.load(rulesfile)
        with open(self.FP['logo']) as logofile:
            self.logo = logofile.read()
        print('ready.')

    def start(self):
        self.menu()

    def menu(self):
        self.seed = '-'.join([hex(ord(x))[2:] for x in
                b64encode(str(randint(0, 100000)).encode()).decode()])
        print(f'{self.PI["N"]} v{self.PI["V"]}:{self.PI["B"]}' +
              f' ☢{game.seed}\n  by {self.PI["A"]}\n')
        print(f'\n\n{self.logo}\n')
        options = ['New Game', 'Exit']
        title = 'Welcome to DungeonWord!'
        self.menuC = Choice(options, title, cmd=['help'])  # "C" means Choice
        self.menuC.display()
        ans = self.menuC.answer()
        if ans == 'New Game':
            self.play()
        else:
            print(f'Unprogrammed function: {ans}')

    def play(self):
        with open(self.FP['rules']) as rulesfile:
            self.rules = json.load(rulesfile)
        while 1:
            self.diffC = Choice([x for x in self.rules],
                                'Choose the difficulty',
                                cmd=['help', 'home'], line='d')
            self.diffC.display()
            ans = self.diffC.answer()
            if ans == 'help':
                Help(self.rules, 'difficulty help')
            elif ans == 'home':
                self.menu()
                break
            else:
                print(f'Unprogrammed function: {ans}')
                


#                                   ┏━━━ S T A R T I N G ━━━┓
#                           = Getting and checking Paths =
paths = Paths('content/paths.json')
paths.check()
FPath = paths.get()

#                           = Registering build =
with open(FPath['build']) as bld:
    BUILD = int(bld.read()) + 1
if inDev:
    with open(FPath['build'], 'w') as bld:
        bld.write(str(BUILD))

game = AVGame(FPath, [AUTHOR, NAME, VERSION, BUILD])
game.start()
