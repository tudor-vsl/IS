from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Util import Counter
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.Random import get_random_bytes
from base64 import b64encode
from base64 import b64decode
import socket
import pickle
from Tema import CBC, OFB,decr_CBC,decr_OFB,char_to_bin,init_iv,xor,bin_to_char

cl_sock=socket.socket()
port = 9999
host = "localhost"
key_K_prime = b'MS\x1en\xea\xd3\xcf2\xd4\xe4\xc7\x9f\x19\xf3\xa1Z'
init_string = "123456789Andreea"

try:
    cl_sock.connect((host, port))
except socket.error as e:
    print(str(e))

#hello
msg_hello=cl_sock.recv(1024)
print(msg_hello.decode("utf-8"))

#text + encryption method
#method_text=cl_sock.recv(1024)
#print(method_text.decode("utf-8"))
method=cl_sock.recv(1024)
print(method.decode("utf-8"))

#iv + key
iv = cl_sock.recv(1024)
print("iv: ", iv)
key_K = cl_sock.recv(1024)
print("key_K: ", key_K)

iv1 = b64decode(iv)
print("iv: ", iv1)

key_K = b64decode(key_K)
cipher = AES.new(key_K_prime, AES.MODE_CBC, iv1)
key_K = unpad(cipher.decrypt(key_K), AES.block_size)
key_k = b64encode(key_K).decode('utf-8')
print("Key K is: ", key_k)

#encryp_list
pck_list = cl_sock.recv(9182)
encryp_list = pickle.loads(pck_list)
print("encryp_list: ",encryp_list)

K_binary = ""

in_ve = init_iv(init_string)
print("in_ve:", in_ve)
for char in str(key_k):
    aux = format(ord(char), 'b')
    while len(aux) != 8:
        aux = '0' + aux
    K_binary += aux

print("K_binary: ", K_binary)



if method.decode("utf-8") == 'CBC':
    plain_list = decr_CBC(K_binary,in_ve,encryp_list)

elif method.decode("utf-8") == 'OFB':
    plain_list = decr_OFB(K_binary,in_ve,encryp_list)

print("plain_list: ", plain_list)
print((bin_to_char(plain_list)))