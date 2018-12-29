import hashlib


m= hashlib.md5()
m.update('qwe123'.encode())
print (m.hexdigest())
