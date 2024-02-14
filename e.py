from base64 import *
SEEDCODE = '4d-54-63-78-4e-7a-49-3d'
print(int(b64decode(''.join([chr(int(x, 16)) for x in SEEDCODE.split('-')]).encode()).decode()))
