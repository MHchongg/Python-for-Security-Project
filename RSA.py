import rsa
import time

public_key, private_key = rsa.newkeys(1024)

print(public_key)

password = "cmhPassword"

start = time.time()
time.sleep(5)
end = time.time()
print("time: ", end - start, " seconds")


encrypted_password = rsa.encrypt(password.encode(), public_key)

plain_password = rsa.decrypt(encrypted_password, private_key)

user_password = input("Enter your password:  ")


if (user_password == plain_password.decode()):
    print("Verification success")
else:
    print("Verification fail")
