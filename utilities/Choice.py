class Choice():
    def __init__(self, options, heading, cmd=[], line='b'):
        self.binds, self.cmd, self.head = {}, cmd, heading
        self.line = line
        for x in range(len(options)):
            self.binds[str(x + 1)] = options[x]
        self.scopes = [f"\"{x}\"" for x in cmd]

    def display(self):
        if self.line == 'b':
            self.out_bold()
        elif self.line == 'd':
            self.out_doub()

    def out_bold(self):
        """Prints choice in bold frame"""
        while 1:
            print(f'\n┏━ {self.head} ━┫▶')
            [print(f'┃{n}. {val}') for n, val in self.binds.items()]
            print('┃')
            if self.cmd:
                print(f'┣ Commands {", ".join(self.scopes)} are available')
            self.ans = input('┗┫')
            self.poss = self.cmd + \
                        [x for x, y in self.binds.items()] + \
                        [y for x, y in self.binds.items()]
            if self.ans in self.poss:
                break

    def out_doub(self):
        """Prints choice in double frame"""
        while 1:
            print(f'\n╔══ {self.head} ══╣▶')
            [print(f'║{n}. {val}') for n, val in self.binds.items()]
            print('║')
            if self.cmd:
                print(f'╠ Commands {", ".join(self.scopes)} are available')
            self.ans = input('╚╣')
            self.poss = self.cmd + \
                        [x for x, y in self.binds.items()] + \
                        [y for x, y in self.binds.items()]
            if self.ans in self.poss:
                break

    def answer(self):
        if self.ans in [y for x, y in self.binds.items()]:
            return self.ans
        elif self.ans in self.binds:
            return self.binds[self.ans]
        elif self.ans in self.cmd:
            return self.ans
        else:
            return ''
