import hashlib
from cryptography.fernet import Fernet
import os


def split_name_extn(file):
    d = file[::-1].find('.')
    e = len(file)
    return file[:e - d - 1], file[e - d:]


def get_fernet(key):
    key_sha = hashlib.sha256(key.encode())
    key_sha_string = key_sha.hexdigest()
    key_sha_string = key_sha_string[:43]
    key_sha_string += '='
    return Fernet(key_sha_string.encode())


def encrypt(fernet, data):
    return fernet.encrypt(data)


def decrypt(fernet, token):
    return fernet.decrypt(token)


def copy_back_to_original(frm_file, to_file):
    with open(frm_file, 'rb') as fin:
        with open(to_file, 'wb') as fout:
            while (i := fin.readline()):
                fout.write(i)
    with open(frm_file, 'w'):
        pass
    os.remove(frm_file)


def copy_encrypt_data(file, fernet):
    print("Encryption in progress ...")
    enc_file, extn = split_name_extn(file)
    enc_file = enc_file + '(enc)'
    with open(file, 'rb') as fin:
        with open(enc_file, 'wb') as fout:
            fout.write((encrypt(fernet, extn.encode()).decode() + '\n').encode())
            while i := fin.readline():
                fout.write((encrypt(fernet, i).decode() + '\n').encode())
    copy_back_to_original(enc_file, file)
    os.rename(file, split_name_extn(file)[0])

def copy_decrypt_data(file, fernet):
    print("Decryption in pregress ...")
    with open(file, 'rb') as fin:
        extn = decrypt(fernet, fin.readline()).decode()
        dec_file = file + '(dec).' + extn
        with open(dec_file, 'wb') as fout:
            while i := fin.readline():
                fout.write(decrypt(fernet, i))
    copy_back_to_original(dec_file, file)
    os.rename(file, file + '.' +extn )

def get_key():
    key1 = input("Enter Key   >> ").strip()
    key2 = input("Reenter Key >> ").strip()
    
    if key1 == key2:
        return key1

    return False

print(" ______________________________________________________________________________________")
print("|                               Encrypt & Decrypt Files                                 |")
print("|                                   by Vignesh Hegde                                    |")
print("|_______________________________________________________________________________________|")
print("| NOTE : There is no option to reset password once lost data cannot be recovered.       |")
print("| This is just a fun project, I am(vignesh hegde) not responsible for any loss of data  |")
print("|_______________________________________________________________________________________|")

file_loc = input("File Name : ").strip()


flag = True

while flag:
    key = get_key()
    if not key:
        print("Key did not match, Try again.")
    else:
        flag = False

flag = True

try:
    fernet = get_fernet(key)
except Exception as e:
    print("Unable to  generate fernet")
    exit()

while flag:
    choice = input("e: encrypt\nd: decrypy\nx: exit\n").strip()
    if choice == 'e' or choice == 'E':
        try:
            flag = False
            copy_encrypt_data(file_loc, fernet)
            input("Completed\nWARNING : Do Not Forget Password !")
        except:
            input("Unable to encrypt")
    elif choice == 'd' or choice == 'D':
        try:
            flag = False
            copy_decrypt_data(file_loc, fernet)
            input("Completed")
        except:
            input("Unable to decrypt")
    elif choice == 'x' or choice == 'X':
        flag = False

