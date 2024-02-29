class WordDisplay():
    def __init__(self, word):
        self.word = word
        self.shown = []

    def show(self, letter):
        if letter in self.word and not (letter in self.shown):
            self.shown.append(letter)
            return True
        return False

    def reveal(self):
        self.shown = list(set(self.word))

    def print(self, title=None, frame=''):
        wordlist = []
        for x in list(self.word):
            if x in self.shown:
                wordlist.append(f'│ {x} │')
            else:
                wordlist.append('│   │')
        bdup = ['┌───┐'] * len(wordlist)
        bdwn = ['└───┘'] * len(wordlist)
        for x in [' '.join(x) for x in [bdup, wordlist, bdwn]]:
            print(frame + x + frame[::-1])

    def done(self):
        if len(set(self.word)) == len(self.shown):
            return True
        return False
