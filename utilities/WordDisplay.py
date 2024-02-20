class WordDisplay():
    def __init__(self, word):
        self.word = word
        self.shown = []

    def show(self, letter):
        if letter in self.word and not (letter in self.shown):
            self.shown.append(letter)

    def reveal(self):
        self.shown = list(set(word))

    def print(self, title=None):
        wordlist = []
        for x in list(self.word):
            if x in self.shown:
                wordlist.append(f'│ {x} │')
            else:
                wordlist.append('│   │')
        bdup = ['┌───┐'] * len(wordlist)
        bdwn = ['└───┘'] * len(wordlist)
        print('\n'.join([' '.join(x) for x in [bdup, wordlist, bdwn]]))
