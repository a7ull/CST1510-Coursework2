import bcrypt

def hash_password(plain_text_pass):
    password_bytes = plain_text_pass.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

passw="apple"
password_hash = hash_password(passw)
print(f'Password hash: {passw},hash,{password_hash}')

