from password_generator import PasswordGenerator


pwo = PasswordGenerator()
pwo.maxlen = 16
pwo.minlen = 16
print(pwo.generate())

