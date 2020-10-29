#imports
import hashlib

#simple functions isolated
def encrypt(password):
    password += "çopademacaco"
    sha_signature = \
        hashlib.sha256(password.encode()).hexdigest()
    return sha_signature