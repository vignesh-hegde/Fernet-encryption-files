




from file_handler import FileHandler
import argparse
from getpass import getpass


def get_file():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', metavar='file', help='Encrypt File')
    parser.add_argument('-d', metavar='file', help='Decrypt File')
    args = parser.parse_args()

    if (args.d == args.e) or (args.d != None and args.e != None):
        return None, None

    return (args.d, "D") if args.d else (args.e, "E")


def get_pass(confirmation_needed = False):
    password_1 =  getpass("Enter password: ")
    
    if confirmation_needed:
        password_2 =  getpass("Confirm password: ")
        if password_1 != password_2:
            return None

    return password_1


if __name__ == "__main__":
    file_name,algo = get_file()
    f = FileHandler()

    if (file_name == None):
        print("Invalid input")
        print("-d <FILE>  OR -e <FILE>")
    else:
        password = get_pass(algo == "E")
        if password == None:
            print("Enter Same password")
        else:
            match algo:
                case "E":
                    f.copy_encrypt_data(file_name, password)
                case "D":
                    f.copy_decrypt_data(file_name, password)
                case _:
                    pass



