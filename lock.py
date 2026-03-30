import os, json, getpass, zipfile
from Crypto.Cipher import AES
from Crypto.Hash import MD5

DIR = os.path.dirname(os.path.abspath(__file__))
ENCODING = "utf-8"
SALT = "fe3&cc8da@tvb_vs"

def read_bin_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        file_data = file.read()
        file.close()
        return file_data

def write_bin_file(file_path: str, data: bytes):
    with open(file_path, 'wb') as file:
        file.write(data)
        file.close()

def encrypt_file(target_path: str, output_path: str):
    write_bin_file(output_path, CIPHER.encrypt(read_bin_file(target_path)))

def zip_folder(folder_path: str, output_path: str):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


def main():
    keyword = getpass.getpass(prompt="Please Input Key>") + SALT
    key = MD5.new(keyword.encode(encoding=ENCODING)).digest()
    global CIPHER
    CIPHER = AES.new(key, AES.MODE_EAX)

    zip_folder(os.path.join(DIR, "files/"), os.path.join(DIR, ".tmp/files.zip"))
    encrypt_file(os.path.join(DIR, ".tmp/files.zip"), os.path.join(DIR, "encrypted_files.bin"))

    print("Encryption Complete!")
    nonce_str = CIPHER.nonce.hex()
    size = 4
    print(f"Number Used Once: 0x {' '.join([nonce_str[i:i+size] for i in range(0, len(nonce_str), size)])}")

if __name__ == "__main__":
    main()
