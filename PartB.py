from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode
import time


def encrypt_decrypt(method, type, password, data):
    if method not in ["AES", "DES", "RSA"]:
        raise ValueError("Invalid encryption method. Please choose AES, DES, or RSA.")

    if type not in ["encrypt", "decrypt"]:
        raise ValueError("Invalid operation type. Please choose encrypt or decrypt.")

    start_time = time.time()  # Record start time

    if method == "RSA" and type == "encrypt":
        # Load RSA public key from file or generate it
        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(), backend=default_backend()
            )

        if isinstance(password, str):
            password = password.encode()

        if type == "encrypt":
            # Encrypt data using RSA public key
            ciphertext = public_key.encrypt(
                password,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            end_time = time.time()  # Record end time
            print("Generation time:", end_time - start_time, "seconds")
            return ciphertext
        else:
            raise ValueError("RSA decryption not supported in this function.")
    else:
        if isinstance(password, str):
            password = password.encode()

        if method == "AES":
            key = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b"salt",
                iterations=100000,
                backend=default_backend(),
            ).derive(password)
            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            if type == "encrypt":
                padder = sym_padding.PKCS7(128).padder()
                padded_data = padder.update(data.encode()) + padder.finalize()
                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(padded_data) + encryptor.finalize()
                end_time = time.time()  # Record end time
                print("Generation time:", end_time - start_time, "seconds")
                return ciphertext
            else:
                unpadder = sym_padding.PKCS7(128).unpadder()
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(data) + decryptor.finalize()
                unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
                end_time = time.time()  # Record end time
                print("Generation time:", end_time - start_time, "seconds")
                return unpadded_data.decode()

        elif method == "DES":
            key = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=8,
                salt=b"salt",
                iterations=100000,
                backend=default_backend(),
            ).derive(password)
            cipher = Cipher(
                algorithms.TripleDES(key), modes.ECB(), backend=default_backend()
            )
            if type == "encrypt":
                padder = sym_padding.PKCS7(64).padder()
                padded_data = padder.update(data.encode()) + padder.finalize()
                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(padded_data) + encryptor.finalize()
                end_time = time.time()  # Record end time
                print("Generation time:", end_time - start_time, "seconds")
                return ciphertext
            else:
                unpadder = sym_padding.PKCS7(64).unpadder()
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(data) + decryptor.finalize()
                unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
                end_time = time.time()  # Record end time
                print("Generation time:", end_time - start_time, "seconds")
                return unpadded_data.decode()


# Example usage
if __name__ == "__main__":
    # Example AES encryption
    aes_encrypted = encrypt_decrypt("AES", "encrypt", "password", "Hello, world!")
    print("AES encrypted:", b64encode(aes_encrypted))
    aes_decrypted = encrypt_decrypt("AES", "decrypt", "password", aes_encrypted)
    print("AES decrypted:", aes_decrypted)

    # Example DES encryption
    des_encrypted = encrypt_decrypt("DES", "encrypt", "password", "Hello, world!")
    print("DES encrypted:", b64encode(des_encrypted))
    des_decrypted = encrypt_decrypt("DES", "decrypt", "password", des_encrypted)
    print("DES decrypted:", des_decrypted)

    # Example RSA encryption
    rsa_encrypted = encrypt_decrypt("RSA", "encrypt", "password", "Hello, world!")
    print("RSA encrypted:", b64encode(rsa_encrypted))
    # RSA decryption is not supported in this function


# Example usage
if __name__ == "__main__":
    # Example AES encryption
    aes_encrypted = encrypt_decrypt("AES", "encrypt", "password", "Hello, world!")
    print("AES encrypted:", b64encode(aes_encrypted))
    aes_decrypted = encrypt_decrypt("AES", "decrypt", "password", aes_encrypted)
    print("AES decrypted:", aes_decrypted)

    # Example DES encryption
    des_encrypted = encrypt_decrypt("DES", "encrypt", "password", "Hello, world!")
    print("DES encrypted:", b64encode(des_encrypted))
    des_decrypted = encrypt_decrypt("DES", "decrypt", "password", des_encrypted)
    print("DES decrypted:", des_decrypted)

    # Example RSA encryption
    rsa_encrypted = encrypt_decrypt("RSA", "encrypt", "password", "Hello, world!")
    print("RSA encrypted:", b64encode(rsa_encrypted))
    # RSA decryption is not supported in this function
