import json
import os
import platform
from base64 import b64encode, b64decode
from utilities.Choice import Choice
from utilities.PathManager import Paths
from utilities.cuts import choose_lang
from utilities.WordDisplay import WordDisplay
from utilities.random import randint
from utilities.Help import Help

'''
 ==  P R O J E C T   I N F O  ==
'''

AUTHOR = 'VovLer Games (DaregonPL)'
NAME = 'DungeonWord'
VERSION = '0.1'


class AVGame():
    """DungeonWord game class"""
    def __init__(self, paths, PI, startdata={}):
        print('|==> GAME INIT <==|')
        self.USER = 'user'
        if platform.system() == 'Windows':
            filepathl = __file__.split('\\')
            self.USER = filepathl[2]
            print('Welcome, ' + filepathl[2])
        else:
            raise TypeError('Windows is required')
        self.sd = startdata
        self.FP = paths
        self.inDev = self.sd['inDev'] if 'inDev' in self.sd else False
        self.PI = {'A': PI[0], 'N': PI[1], 'V': PI[2], 'B': PI[3]}
        os.makedirs('content/progress', exist_ok=True)
        with open(self.FP['rules']) as rulesfile:
            self.rules = json.load(rulesfile)
        with open(self.FP['logo']) as logofile:
            self.logo = logofile.read()
        with open(self.FP['fail']) as logofile:
            self.FailI = logofile.read()
        with open(self.FP['win']) as logofile:
            self.WinI = logofile.read()
        with open(self.FP['VLL']) as logofile:
            self.VLlogo = logofile.read()
        with open(self.FP['dicts']) as dictsfile:
            self.dicts = json.load(dictsfile)
        with open(self.FP['settings']) as settsfile:
            self.setts = json.load(settsfile)
            self.settingdict = self.setts['options']
        print('ready.')

    def start(self):
        print(f'{self.PI["N"]} v{self.PI["V"]}:{self.PI["B"]}' +
              f'\n  by {self.PI["A"]}\n')
        if not os.path.exists(f'content/progress/{self.USER}.user'):
            with open(f'content/progress/{self.USER}.user', 'w') as userfile:
                json.dump({'user': self.USER, 'score': 0}, userfile)
        with open(f'content/progress/{self.USER}.user') as usrf:
            self.userdata = json.load(usrf)
        self.menu()

    def menu(self):
        self.seed = '-'.join([hex(ord(x))[2:] for x in
                              b64encode(str(randint(0, 100000))
                                        .encode()).decode()])
        dic = b64decode
        print(f'\n\n{self.logo}\n')
        print(f'User:{self.userdata["user"]}  Score:{self.userdata["score"]}')
        options = ['Play', 'Reset', 'Save & Exit']
        title = 'Welcome to DungeonWord!'
        self.menuC = Choice(options, title, cmd=['help'],
                            hide=[{'cmd': 'decrypt', 'args':
                                   ['seed', 'lang', 'diff']},
                                  {'cmd': 'get', 'args': ['word']},
                                  {'cmd': 'cfg', 'args': ['param']}])
        # "C" means Choice
        while 1:
            self.menuC.display()
            ans = self.menuC.answer()
            if ans == 'Play':
                self.play()
                break
            elif ans == 'Save & Exit':
                with open(f'content/progress/{self.USER}.user', 'w') as usrf:
                    json.dump(self.userdata, usrf, indent=4)
                print(f'Saved to {self.USER}.user')
                break
            elif ans == 'Reset':
                if os.path.exists(f'content/progress/{self.USER}.user'):
                    os.remove(f'content/progress/{self.USER}.user')
                    print('SaveData file removed')
                break
            elif ans == 'help':
                print(f'\n{self.PI["N"]} v{self.PI["V"]}:{self.PI["B"]}' +
                      f'   ☢{game.seed}\n  by {self.PI["A"]}')
                print('\nRemake for classic game "Guess The Word"')
                print('Here you need to guess the word based on the')
                print('letters you\'ve already guessed and on word\'s lenght')
                print(' '.join('\n Made by\n'.upper()) + self.VLlogo)
            
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
            elif type(ans) is dict and ans['cmd'] == 'cfg':
                vals = ans['args']
                if vals['param'] == '*':
                    print(['seed', 'symdol'] + [x for x in self.settingdict])
                elif vals['param'] == 'seed':
                    if 'seed' in vals:
                        self.seed = '-'.join([hex(ord(x))[2:] for x in
                                      b64encode(str(ans['args']['seed'])
                                                .encode()).decode()])
                        print(f'Updated seed: ☢{self.seed}')
                    else:
                        print('seed expected, got', ', '.join
                              ([x for x in vals]))
                elif vals['param'] == 'symbol':
                    symcon = Choice([x for x in self.setts['symbols']],
                                    '-symbol.config.disp')
                    symcon.display()
                    ans = symcon.answer()
                    smbl = input(ans + '.set:')
                    print(chr(self.setts['symbols'][ans]), '->', smbl)
                    self.setts['symbols'][ans] = ord(smbl)
                    with open(self.FP['settings'], 'w') as settsfile:
                        json.dump(self.setts, settsfile, indent=4)
                    print('saved.')
                elif vals['param'] in self.settingdict:
                    if 'value' in vals:
                        if vals['value'] in ['1', '0', 'false', 'true']:
                            value = True if vals['value'] in ['1', 'true'] \
                                    else False
                            print(vals['param'] + ':', value)
                            self.settingdict[vals['param']] = vals['value']
                            self.setts['options'] = self.settingdict
                            with open(self.FP['settings'], 'w') as settsfile:
                                json.dump(self.setts, settsfile, indent=4)
                        else:
                            print('value must be int or bool')
                    else:
                        print('value expected, got', ', '.join
                              ([x for x in vals]))
                else:
                    print('Cannot access', vals['param'])
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
        print('Searching a word for you...')
        gameseed = int(b64decode(''.join([chr(int(x, 16))
                                          for x in game.seed.split('-')])
                                 .encode()).decode())
        self.Word = self.get_word(gameseed, self.diff, self.lang)
        if self.inDev:
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
        self.lifes = self.crits['attempts']
        self.letts = []
        err = ''
        failed, att = 0, 0
        while not self.disp.done() and not failed:
            if self.settingdict['heartsDisplay']:
                lfs = ' '.join("♥" * (self.lifes - att) + "♡" * att) \
                      if self.lifes != -1 else "∞"
            else:
                lfs = self.lifes - att if self.lifes != -1 else "∞"
            print('')
            self.disp.print(frame='▣ ▍▎▏  ')
            print(f'\n Lifes: {lfs}')
            print(f' Mistakes: {att}\n')
            print('/help - list of commands')
            print(f'Message: {err}')
            print('=', ' '.join([x if x not in self.letts else
                            ' ' for x in self.accepted]), '=')
            ans = input('>>>').lower()
            if ans == '/q':
                failed = True
                continue
            elif ans == '/used':
                print('Used:', ' '.join(self.letts))
                continue
            elif ans == '/help':
                cmd = {'/q': 'Quit', '/used': 'Used symbols', '/help': 'Commands'}
                print('    Game Commands:')
                [print(f'{x}: \t{y}') for x, y in cmd.items()]
                continue
            # Unsort invalid
            if len(ans) != 1:
                err = 'one letter is expected'
                continue
            elif not (ans in self.accepted):
                err = f'error 49300: use {self.lang} letters'
                continue
            elif ans in self.letts:
                err = f'You\'ve already used this letter ({ans})'
                continue
            else:
                err = ''
            # Checking
            if not self.disp.show(ans.upper()):
                att += 1
            if not (ans in self.letts):
                self.letts.append(ans)
                self.letts.sort()
            if att == self.lifes:
                failed = True
        if not failed:
            print(self.WinI)
        else:
            print(self.FailI)
        print('')
        self.disp.reveal()
        self.disp.print(frame='│║◈║│ ')
        self.userdata['score'] += self.crits['reward']
        print(f'Attempts: {len(self.letts)}, Score: {self.crits["reward"]}')

    def get_word(self, seed, diff, lang):
        with open(self.dicts[lang]['path'], encoding='utf-8') as langfile:
            self.words = langfile.read().split('\n')
        self.crits = self.rules[diff]
        self.accepted = [chr(x) for x in range(self.dicts[lang]['range'][0],
                                               self.dicts[lang]['range'][1])]
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

#                           = Registering build =
with open(FPath['build']) as bld:
    BUILD = int(bld.read()) + 1
if confs['inDev']:
    with open(FPath['build'], 'w') as bld:
        bld.write(str(BUILD))

game = AVGame(FPath, [AUTHOR, NAME, VERSION, BUILD], confs)
game.start()
