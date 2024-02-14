def Help(helpDict, title):
    ex = ' '.join([x.upper() for x in title])
    print(f'\n┏━━━ {ex} ━━━┓')
    for x, y in helpDict.items():
        print(f'\n{x}:')
        if type(y) is dict:
            for name, value in y.items():
                if name == 'attempts':
                    name = 'Mistakes amount'
                if name == 'MinLenght':
                    name = 'Minimum lenght'
                if name == 'MaxLenght':
                    name = 'Maximum lenght'
                print(f'  {name}: {value}')
