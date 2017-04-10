from Crypto.Cipher import DES3
from Crypto import Random
import sys

cookie = "ABCDEFGH"

data  = "GET / HT"
data += "TP/1.1\r\n"
data += "Host: ww"
data += "w.ab.ro\r"
data += "\nCookie:"
data += " secret="
data += 9 * cookie
data += "\r\nAccept"
data += ": text/p"
data += "lain\r\n\r\n"

SECRET_KEY = b'-8B key--8B key-'

# clientul va randomiza headere inainte de trimiterea requestului
# serverul va accepta requesturile, deoarece standardul HTTP nu impune o ordine a headerelor
from Crypto.Random import random

def shuffle_headers(request_text):
    lines = request_text.split('\r\n')
    method = lines[:1]
    headers = lines[1:4]
    ending = lines[4:]

    # shuffle headers
    random.shuffle(headers)

    return "\r\n".join(method + headers + ending)

def _make_des3_encryptor(key, iv):
    encryptor = DES3.new(key, DES3.MODE_CBC, iv)
    return encryptor


def des3_encrypt(key, iv, data):
    assert len(data) % 8 == 0
    assert len(iv) % 8 == 0

    encryptor = _make_des3_encryptor(key, iv)
    return encryptor.encrypt(data)


def des3_decrypt(key, iv, data):
    assert len(data) % 8 == 0
    assert len(iv) % 8 == 0

    encryptor = _make_des3_encryptor(key, iv)
    result = encryptor.decrypt(data)
    return result


def encrypt_request(request_payload):
    random_iv = Random.new().read(8)

    ciphertext = des3_encrypt(SECRET_KEY, random_iv, request_payload)
    return random_iv + ciphertext

def decrypt_request(iv_and_ciphertext):
    random_iv = iv_and_ciphertext[:8]
    ciphertext = iv_and_ciphertext[8:]

    request_data = des3_decrypt(SECRET_KEY, random_iv, ciphertext)
    return request_data

def generate_request_ciphertext(REQUEST, messages_number, f):
    for i in xrange(messages_number):

        if i % 100 == 0:
            print "writing message number: %s" % i

        ciphertext = encrypt_request(REQUEST)
        f.write(ciphertext)

#ciphertext = encrypt_request(REQUEST)
#message = decrypt_request(ciphertext)

if __name__ == "__main__":
    f = open(sys.argv[1], 'wb')

    n = 247243184 / 4
    request_shuffled = shuffle_headers(data)
    generate_request_ciphertext(request_shuffled, n, f)

    f.close()
