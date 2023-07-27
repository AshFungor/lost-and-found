from cryptography.fernet import Fernet
import hashlib
import sys
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


BLOCK_SIZE  =   2 ** 17
MAIN_KEY    =   b'SCacvTazGALipT1MpEeaPf0X4xHz6OPNKXWiy8BUrSI='
FILES       =   {'intro.encrypted'              : b'/\x04\x1bN\xba\xd3\x07\xbb\xee\x88\x17\x0cd=\xdd\xfe'   , 
                'stars_are_right.encrypted'     : b'?\xdc\xb4\xf8v\xa1\r\x89\x1d\x1f7\x01\x9c\t\xad\xe0'    ,
                'luck_of_the_draw.encrypted'    : b')\xfa\x08\x0c/\xb1\xfb6f\x96\x8c8!E\xd1\xec'            ,
                'last_message.encrypted'        : b',)\x9fx#\xc1\x9f\x8e\x82\xc5\xd9\x16c\x86\xf7\xfb'      ,
                'DELETE_THIS.encrypted'         : b'\xd52\x10^\xb12\xcfW\x1b;G\xf5\xd7r\xe0\xac'            }

def encrypt(file, key):
    with open(file, 'rb') as in_file, open(file[:file.rfind('.')] + '.encrypted', 'wb') as out_file:
        data = bytes()
        while True:
            block = in_file.read(BLOCK_SIZE)
            data += block
            if not block:
                break
            f = Fernet(key)
            output = f.encrypt(block)
            out_file.write(len(output).to_bytes(16))
            out_file.write(output)
        out_file.write(int(0).to_bytes(16))

def decrypt(file, key):
    in_file = open(file, 'rb')
    out_filename = file.replace('.encrypted', '.zip')
    out_file = open(out_filename, 'wb')
    data = bytes()
    while True:
        block_size = int.from_bytes(in_file.read(16))
        if not block_size:
            break
        block = in_file.read(block_size)
        f = Fernet(key)
        output = f.decrypt(block)
        out_file.write(output)
        data += output
    in_file.close()
    out_file.close()

def derive_key(file, password):
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=FILES[file],
            iterations=480_000,
            )
    return base64.urlsafe_b64encode(kdf.derive(password.encode('UTF-8')))


if __name__ == '__main__':
    encrypt(os.getcwd() + '/../assets/intro.zip', MAIN_KEY)
    key_1 = derive_key('stars_are_right.encrypted', 'buer')
    encrypt(os.getcwd() + '/../assets/stars_are_right.zip', key_1)
    key_2 = derive_key('luck_of_the_draw.encrypted', 'abigor')
    encrypt(os.getcwd() + '/../assets/luck_of_the_draw.zip', key_2)
    key_3 = derive_key('last_message.encrypted', 'alastor')
    encrypt(os.getcwd() + '/../assets/last_message.zip', key_3)
    key_4 = derive_key('DELETE_THIS.encrypted', 'azazel')
    encrypt(os.getcwd() + '/../assets/DELETE_THIS.zip', key_4)
