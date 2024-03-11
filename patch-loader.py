import os
from json import load, dump
from utilities.Choice import Choice


def start():
    global dwpatch
    print(dwpatch)
    mnu = Choice(['New Patch', 'Uninstall Patch', 'Exit'], 'Menu')
    mnu.display()
    ans = mnu.answer()
    if ans == 'New Patch':
        newpatch()
        start()
    elif ans == 'Uninstall Patch':
        delpatch()
        start()
    elif ans == 'Exit':
        print('/')
    else:
        print('unprog.')
        start()

def newpatch():
    data = {}
    while 1:
        print("Name for patch:")
        name = input('<str>')
        if name.isalnum():
            break
        elif not name:
            raise KeyboardInterrupt('cancel')
        else:
            print('name can only consist alpha and digits')
    while 1:
        print('Enter words below (leave blank when you done):')
        words = ''
        a = input()
        while a:
            words += a + '\n'
            a = input()
        exc = [x for x in words.split() if not x.isalpha()]
        if exc:
            print('use letters only')
        elif not words:
            raise KeyboardInterrupt('cancel')
        else:
            words = words.lower().split()
            print(f'First: {words[0]}\nLast: {words[-1]}')
            data['path'] = f'words/{name.lower()}.dict'
            break
    langc = Choice(['English letters', 'Russian letters'], 'Choose package of letters', cmd=['cancel'])
    langc.display()
    ans = langc.answer()
    if ans == 'cancel':
        raise KeyboardInterrupt('cancel')
    elif ans == 'English letters':
        data['range'] = [97, 123]
    elif ans == 'Russian letters':
        data['range'] = [1072, 1104]
    data['enabled'] = False
    # saving
    with open('content/patch.json') as patchfile:
        a = load(patchfile)
        a[name] = data
    with open('content/patch.json', 'w') as patchfile:
        dump(a, patchfile, indent=4)
    with open(data['path'], 'w') as dictfile:
        dictfile.write('\n'.join(words))
    print('saved')

def delpatch():
    with open('content/patch.json') as patchfile:
        ptchs = load(patchfile)
    patchesC = Choice([x for x in ptchs], 'Choose a patch to uninstall', cmd=['cancel'])
    patchesC.display()
    ans = patchesC.answer()
    if ans == 'cancel':
        raise KeyboardInterrupt('cancel')
    else:
        data = ptchs.pop(ans)
        os.remove(data['path'])
        with open('content/patch.json', 'w') as patchfile:
            dump(ptchs, patchfile, indent=4)
    print('deleted')

#  Introduction
print('Patch-loader v1\n\tby VovLer G.')

dwpatch = r'''

 ____    __      __                             __           __         
/\  _`\ /\ \  __/\ \                           /\ \__       /\ \        
\ \ \/\ \ \ \/\ \ \ \           _____      __  \ \ ,_\   ___\ \ \___    
 \ \ \ \ \ \ \ \ \ \ \  _______/\ '__`\  /'__`\ \ \ \/  /'___\ \  _ `\  
  \ \ \_\ \ \ \_/ \_\ \/\______\ \ \_\ \/\ \_\.\_\ \ \_/\ \__/\ \ \ \ \ 
   \ \____/\ `\___ ___/\/______/\ \ ,__/\ \__/.\_\\ \__\ \____\\ \_\ \_\
    \/___/  '\/__//__/           \ \ \/  \/__/\/_/ \/__/\/____/ \/_/\/_/  
                                  \ \_\                                 
                                   \/_/
                                    
'''
start()
