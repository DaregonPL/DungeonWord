import json
from base64 import b64encode, b64decode
from utilities.Choice import Choice
from utilities.PathManager import Paths
from utilities.cuts import choose_lang
from utilities.WordDisplay import WordDisplay
from utilities.random import randint

'''
 ==  P R O J E C T   I N F O  ==
'''

AUTHOR = 'VovLer Games (DaregonPL)'
NAME = 'DungeonWord'
VERSION = '0.1'


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
        with open(self.FP['rules']) as rulesfile:
            self.rules = json.load(rulesfile)
        with open(self.FP['dicts']) as dictsfile:
            self.dicts = json.load(dictsfile)
        print('ready.')

    def start(self):
        print(f'{self.PI["N"]} v{self.PI["V"]}:{self.PI["B"]}' +
              f'\n  by {self.PI["A"]}\n')
        self.menu()

    def menu(self):
        self.seed = '-'.join([hex(ord(x))[2:] for x in
                              b64encode(str(randint(0, 100000))
                                        .encode()).decode()])
        dic = b64decode
        print(f'\n\n{self.logo}\n')
        options = ['New Game', 'Exit']
        title = 'Welcome to DungeonWord!'
        self.menuC = Choice(options, title, cmd=['help'],
                            hide=[{'cmd': 'decrypt', 'args':
                                   ['seed', 'lang', 'diff']},
                                  {'cmd': 'get', 'args': ['word']},
                                  {'cmd': 'set', 'args': ['seed']}])
        # "C" means Choice
        while 1:
            self.menuC.display()
            ans = self.menuC.answer()
            if ans == 'New Game':
                self.play()
                break
            elif ans == 'Exit':
                print('Saved to !NOFILEFOUND')
                break
            elif ans == 'help':
                print(f'\n{self.PI["N"]} v{self.PI["V"]}:{self.PI["B"]}' +
                      f'   ☢{game.seed}\n  by {self.PI["A"]}')
                print('\nRemake for classic game "Guess The Word"')
                print('Here you need to guess the word based on the')
                print('letters you\'ve already guessed and on word\'s lenght')
            elif type(ans) is dict and ans['cmd'] == 'decrypt':
                if ans['args']['seed'][0] == '☢':
                    cutSeed = ans['args']['seed'][1:]
                    cutLang = ans['args']['lang']
                    cutDiff = ans['args']['diff']
                    code = int(dic(''.join([chr(int(x, 16)) for x in
                                            cutSeed.split('-')])
                                   .encode()).decode())
                    print(f'Seed: {code}-{cutLang}-{cutDiff}')
            elif type(ans) is dict and ans['cmd'] == 'get':
                if ans['args']['word']:
                    data = ans['args']['word'].split('-')
                    code, lang, diff = int(data[0]), data[1], data[2]
                    if lang in self.dicts and diff in self.rules:
                        print('W:' + self.get_word(code, diff, lang))
                    else:
                        print('unregistered data')
            elif type(ans) is dict and ans['cmd'] == 'set':
                self.seed = '-'.join([hex(ord(x))[2:] for x in
                              b64encode(str(ans['args']['seed'])
                                        .encode()).decode()])
                print(f'Updated seed: ☢{self.seed}')
            else:
                print(f'Unprogrammed function: {ans}')

    def play(self):
        self.langC = Choice([x for x in self.dicts],
                            'Choose language',
                            cmd=['home'], line='d')
        self.diffC = Choice([x for x in self.rules],
                            'Choose difficulty',
                            cmd=['help', 'home'], line='d')
        choose_lang(self)

    def begin(self):
        global inDev
        print('Searching a word for you...')
        gameseed = int(b64decode(''.join([chr(int(x, 16))
                                          for x in game.seed.split('-')])
                                 .encode()).decode())
        self.Word = self.get_word(gameseed, self.diff, self.lang)
        if inDev:
            print(f'Crits: {self.crits}')
            print(f'Fits: {len(self.goodwords)} / {len(self.words)}' +
                  f'({int(len(self.goodwords)/len(self.words)*100)}%)')
            print(f'Seed: {self.seed}({gameseed})')
            print(f'Index: InFit:{self.goodwords.index(self.Word)},' +
                  f' All:{self.words.index(self.Word)}')
            print(f'Word: {self.Word}')
        self.guess(self.Word)
        input()
        self.menu()

    def guess(self, word):
        self.disp = WordDisplay(word.upper())
        guessed, failed = 0, 0
        while not guessed and not failed:
            self.disp.print()
            break

    def get_word(self, seed, diff, lang):
        with open(self.dicts[lang], encoding='utf-8') as langfile:
            self.words = langfile.read().split('\n')
        self.crits = self.rules[diff]
        self.minLen = self.crits['MinLenght'] if 'MinLenght' in \
            self.crits else 0
        self.maxLen = self.crits['MaxLenght'] if 'MaxLenght' in \
            self.crits else 999999
        self.goodwords = []
        for word in self.words:
            if self.minLen <= len(word) <= self.maxLen:
                self.goodwords.append(word)
        return self.goodwords[seed % len(self.goodwords) - 1]


#                                   ┏━━━ S T A R T I N G ━━━┓
#                           = Getting and checking Paths =
paths = Paths('content/paths.json')
paths.check()
FPath, confs = paths.get()
inDev = confs['inDev']

#                           = Registering build =
with open(FPath['build']) as bld:
    BUILD = int(bld.read()) + 1
if inDev:
    with open(FPath['build'], 'w') as bld:
        bld.write(str(BUILD))

game = AVGame(FPath, [AUTHOR, NAME, VERSION, BUILD])
game.start()
