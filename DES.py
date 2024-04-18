from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

password = "cmhPassword"
key = get_random_bytes(8)
print("key", key)
print(type(key))

cipher = DES.new(key, DES.MODE_ECB)
padded_password = pad(password.encode(), DES.block_size)
encrypted_password = cipher.encrypt(padded_password)

print("Encrypted password:", encrypted_password)
print(type(encrypted_password))

cipher = DES.new(key, DES.MODE_ECB)
decrypted_password = cipher.decrypt(encrypted_password)
unpadded_message = unpad(decrypted_password, DES.block_size).decode()

print("Decrypted password:", unpadded_message)
print(type(unpadded_message))
