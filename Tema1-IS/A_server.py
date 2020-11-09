from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Util import Counter
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.Random import get_random_bytes
from base64 import b64encode
from base64 import b64decode
import json
import socket
from _thread import *
import random
import pickle
from Tema import CBC, OFB,decr_CBC,decr_OFB,char_to_bin,init_iv

global key_enc
global iv
global key_K1

key_enc = ""
iv1 = ""
init_string = "123456789Andreea"
plaintext = "It was my second day on the job. I was sitting in my seemingly gilded cubicle, overlooking Manhattan, " \
                    "and pinching my right arm to make sure it was real. I landed an internship at Conde Nast Traveler. " \
                    "Every aspiring writer I have ever known secretly dreamt of an Anthony Bourdain lifestyle. " \
                    "Travel the world and write about its most colorful pockets. When my phone rang, and it was Mom telling " \
                    "me Dad had a heart attack. He did not make it. I felt as though the perfectly carpeted floors had dropped" \
                    " out from under me. Now that I have come out the other side, I realize Dad left me with a hefty stack of " \
                    "teachings. Here are three ideals I know he would have liked for me to embrace."


key_K_prime = b'MS\x1en\xea\xd3\xcf2\xd4\xe4\xc7\x9f\x19\xf3\xa1Z'

def encryption(mode,plaintext):
    print("str(key_enc): ", str(key_K1))
    K_binary = ""
    # aux = str(key_K1)

    for char in str(key_K1):
        aux = format(ord(char), 'b')
        while len(aux) != 8:
            aux = '0' + aux
        K_binary += aux

    print("K_binary: ", K_binary)
    in_ve = init_iv(init_string)

    if mode == 'CBC':
        cyper_list = CBC(K_binary, in_ve, plaintext)
    elif mode == 'OFB':
        cyper_list = OFB(K_binary, in_ve, plaintext)

    print("cyper_list:", cyper_list)
    return cyper_list


def node_client(client,node):


    msg = str('Hello node ' + str(node) + ' !')
    client.send(str.encode(msg))
    key_K = ""
    if node == 'KM':
        client.send(str.encode("[KM] A send: Pass me key K"))

        iv = client.recv(1024)
        key_k = client.recv(1024)

        print('The iv is: ', iv)
        print('The key K ciphered is: ', key_k)
        print('key_K_prime: ', key_K_prime)

        list_glob = globals()
        list_glob["key_enc"] = key_k
        list_glob["iv1"] = iv

        iv = b64decode(iv)
        print("iv: ",iv )
        key_k = b64decode(key_k)
        #print("key_k: ", key_k)
        cipher = AES.new(key_K_prime, AES.MODE_CBC, iv)
        key_k = unpad(cipher.decrypt(key_k), AES.block_size)
        print("The message was pt: ", key_k)
        key_K = b64encode(key_k).decode('utf-8')
        print("Key K is: ", key_K)

        list_glob["key_K1"] = key_K

    if node == 'B':
        #client.send(str.encode("[B] A send: The encryption method is: "))
        list_AES = ['CBC','OFB']
        aes_mode = random.randrange(0,2)
        client.send(str.encode(list_AES[aes_mode]))
        print("iv1: ", iv1)
        #client.send(str.encode("[B] A send: The iv is: "))
        client.send(iv1)
        print("key_enc: ", key_enc)
        #client.send(str.encode("[B] A send: The key is: "))
        client.send(key_enc)
        #client.send(str.encode("Cyperlist"))
        encryp_list = encryption(list_AES[aes_mode],plaintext)
        pck_list = pickle.dumps(encryp_list)
        client.send(pck_list)

    client.close()

sv_sock = socket.socket()
host = 'localhost'
port = 9999

try:
    sv_sock.bind((host, port))
except socket.error as e:
    print(str(e))

print("[A] Listening...")
sv_sock.listen(5)



ok = False
while True:
    client, addr = sv_sock.accept()
    print("connected to: " + str(addr[0]) + ":" + str(addr[1]))
    if ok == False:
        start_new_thread(node_client, (client,'KM'))
        ok = True
    elif ok ==True:
        start_new_thread(node_client, (client, 'B'))

sv_sock.close()