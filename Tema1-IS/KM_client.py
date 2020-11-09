import socket
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Util import Counter
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.Random import get_random_bytes
from base64 import b64encode
from base64 import b64decode
import json

cl_sock=socket.socket()
port = 9999
host = "localhost"

try:
    cl_sock.connect((host, port))
except socket.error as e:
    print(str(e))

K_prime = b'MS\x1en\xea\xd3\xcf2\xd4\xe4\xc7\x9f\x19\xf3\xa1Z'  # K prime

key_K = get_random_bytes(12)                                    # make the K key random
print("key_K: ", key_K)


key_K_format = b64encode(key_K).decode('utf-8')
print("key_K_format: ", key_K_format)

cipher = AES.new(K_prime, AES.MODE_CBC)                        # encoding of K with K_prime
ct_bytes = cipher.encrypt(pad(key_K, AES.block_size))

iv =  b64encode(cipher.iv).decode('utf-8')                     #encoding the iv and the encoded key K
ct = b64encode(ct_bytes).decode('utf-8')


msg=cl_sock.recv(1024)
print(msg.decode("utf-8"))

msg=cl_sock.recv(1024)
print(msg.decode("utf-8"))

print("key_K: ", key_K)
print("iv:", iv)

cl_sock.send(str.encode(iv))
cl_sock.send(str.encode(ct))