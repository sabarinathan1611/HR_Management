import hashlib
from Crypto.Cipher import AES
import configparser

# Function to read the password from the config file
def read_password_from_config():
        config_file='config.ini'
        config = configparser.ConfigParser()
        config.read(config_file)
        password = config.get('Encryption', 'password')
        return password
    

 # Function to pad data to a multiple of AES block size
def pad_data(data):
     block_size = AES.block_size
     padding = block_size - (len(data) % block_size)
     return data + bytes([padding] * padding)
 # Function to encrypt the file
def encrypt_file(input_filename, output_filename, password):
     with open(input_filename, 'rb') as file:
         data = file.read()
     # Compute SHA256 hash of the password to use as a key
     key = hashlib.sha256(password.encode()).digest()
     # Initialize AES cipher with the key
     cipher = AES.new(key, AES.MODE_ECB)
     # Pad the data and encrypt
     encrypted_data = cipher.encrypt(pad_data(data))
     with open(output_filename, 'wb') as file:
         file.write(encrypted_data)


 # Function to unpad data after decryption
def unpad_data(data):
     padding = data[-1]
     return data[:-padding]
 # Function to decrypt the file
def decrypt_file(input_filename, output_filename, password):
     with open(input_filename, 'rb') as file:
         encrypted_data = file.read()
     # Compute SHA256 hash of the password to use as a key
     key = hashlib.sha256(password.encode()).digest()
     # Initialize AES cipher with the key
     cipher = AES.new(key, AES.MODE_ECB)
     # Decrypt the data and unpad
     decrypted_data = unpad_data(cipher.decrypt(encrypted_data))
     with open(output_filename, 'wb') as file:
         file.write(decrypted_data)
