def choose_lang(self):
    self.langC.display()
    ans = self.langC.answer()
    if ans == 'home':
        self.menu()
    elif ans in self.dicts:
        self.lang = self.dicts[ans]
        choose_diff(self)
    else:
        print(f'Unprogrammed function: {ans}')
        choose_lang(self)

def choose_diff(self):
    self.diffC.display()
    ans = self.diffC.answer()
    if ans == 'help':
        Help(self.rules, 'difficulty help')
    elif ans == 'home':
        self.menu()
    elif ans in self.rules:
        self.diff = ans
        self.begin()
    else:
        print(f'Unprogrammed function: {ans}')
        choose_diff(self)
