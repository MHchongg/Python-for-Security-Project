from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

password = "cmhPassword"
key = get_random_bytes(16)
print(key)
print(type(key))

cipher = AES.new(key, AES.MODE_ECB)
padded_password = pad(password.encode(), AES.block_size)
encrypted_password = cipher.encrypt(padded_password)
print(encrypted_password)
print(type(encrypted_password))

cipher = AES.new(key, AES.MODE_ECB)
decrypted_password = cipher.decrypt(encrypted_password)
unpadded_password = unpad(decrypted_password, AES.block_size).decode()
print(unpadded_password)
print(type(unpadded_password))