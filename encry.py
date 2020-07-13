from cryptography.fernet import Fernet
import sys

# Fernet hash key genereted by *Fernet.generate_key()
key = b"kf9q62Hg3SG0JWdz0XwcJgRR4euBd6hL4tAyg--0VQ4="


# encryptor functiont that take plain text password and turn it into hashed bytes string
def Encryptor(key_str, password):
    sys.dont_write_bytecode = True
    encrypted_password = Fernet(key_str).encrypt(bytes(password, 'UTF-8'))
    return encrypted_password

# Decryption functin that turn hased bytes string and reverse it back to string
def Decryptor(key_str, encrypted_password):
    sys.dont_write_bytecode = True
    plain_password = Fernet(key_str).decrypt(encrypted_password)
    return plain_password.decode('UTF-8')
