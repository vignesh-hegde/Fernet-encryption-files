from os import remove as os_remove
from os import rename as os_rename
from crypto import Crypt

class FileHandler:
    def __init__(self):
        self.__crypto_handler = Crypt();

    @classmethod
    def __split_name_extn(cls, file):
        d = file[::-1].find('.')
        e = len(file)
        return file[:e - d - 1], file[e - d:]

    @classmethod
    def __copy_back_to_original(cls, frm_file, to_file):
        with open(frm_file, 'rb') as fin:
            with open(to_file, 'wb') as fout:
                while (i := fin.readline()):
                    fout.write(i)
        with open(frm_file, 'w'):
            pass
        os_remove(frm_file)

    def copy_encrypt_data(self, file_name, key):
        enc_file, extn = self.__split_name_extn(file_name)
        enc_file = f"{enc_file}(enc)"
        with open(file_name, 'rb') as fin:
            with open(enc_file, 'wb') as fout:
                fout.write(f"{self.__crypto_handler.encrypt(extn.encode(), key).decode()}\n".encode())
                while i := fin.readline():
                    fout.write(f"{self.__crypto_handler.encrypt(i, key).decode()}\n".encode())
        FileHandler.__copy_back_to_original(enc_file, file_name)
        os_rename(file_name, self.__split_name_extn(file_name)[0])
    
    def copy_decrypt_data(self, file_name, key):
        with open(file_name, 'rb') as fin:
            extn = self.__crypto_handler.decrypt(fin.readline(), key).decode()
            dec_file = file_name + '(dec).' + extn
            with open(dec_file, 'wb') as fout:
                while i := fin.readline():
                    fout.write(self.__crypto_handler.decrypt(i, key))

        FileHandler.__copy_back_to_original(dec_file, file_name)
        os_rename(file_name, file_name + '.' +extn )