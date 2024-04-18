import hashlib
import os
import random
import string

def hash_password(password):
    salt = "".join(random.choices(string.hexdigits, k=32))
    password_salt = (password + salt).encode("utf-8")
    hash_object = hashlib.sha256(password_salt)
    hashed_password = hash_object.hexdigest()
    return hashed_password, salt

def check_password(password, saved_hashed_password, salt):
    password_salt = (password + salt).encode("utf-8")
    hash_object = hashlib.sha256(password_salt)
    hashed_password = hash_object.hexdigest()
    return hashed_password == saved_hashed_password