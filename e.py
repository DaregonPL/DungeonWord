from base64 import *
SEEDCODE = '4e-54-59-34-4f-41-3d-3d'
print(int(b64decode(''.join([chr(int(x, 16)) for x in SEEDCODE.split('-')]).encode()).decode()))
