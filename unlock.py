import os, shutil, json, getpass, zipfile
from Crypto.Cipher import AES
from Crypto.Hash import MD5

DIR = os.path.dirname(os.path.abspath(__file__))
ENCODING = "utf-8"

def read_bin_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        file_data = file.read()
        file.close()
        return file_data

def write_bin_file(file_path: str, data: bytes):
    with open(file_path, 'wb') as file:
        file.write(data)
        file.close()

def decrypt_file(target_path: str, output_path: str):
    write_bin_file(output_path, CIPHER.decrypt(read_bin_file(target_path)))

def unzip_folder(zipfile_path, output_path):
    with zipfile.ZipFile(zipfile_path, 'r') as zipf:
        zipf.extractall(output_path)

def main():
    keyword = getpass.getpass(prompt="Please Input Key>").encode(encoding=ENCODING)
    key = MD5.new(keyword).digest()
    nonce_str = getpass.getpass(prompt="Please Input Number Used Once>")
    nonce_str.replace(" ", "")
    nonce = bytes.fromhex(nonce_str[2:] if nonce_str[0:2]=="0x" else nonce_str)
    global CIPHER
    CIPHER = AES.new(key, AES.MODE_EAX, nonce=nonce)

    old_files_dir = os.path.join(DIR, "old_files/")
    files_dir = os.path.join(DIR, "files/")
    if os.path.exists(old_files_dir):
        shutil.rmtree(old_files_dir)
    os.rename(files_dir, old_files_dir)
    os.mkdir(files_dir)

    decrypt_file(os.path.join(DIR, "encrypted_files.bin"), os.path.join(DIR, ".tmp/files.zip"))
    unzip_folder(os.path.join(DIR, ".tmp/files.zip"), files_dir)

    print("Decryption Complete!")

if __name__ == "__main__":
    main()
