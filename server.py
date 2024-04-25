from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import rsa
import time
from Crypto.Cipher import DES, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
CORS(app)

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="python_user")

mycursor = mydb.cursor(dictionary=True)


def encryptPassword(method, password, extra):
    match method:
        case "rsa":
            encrypted_password = rsa.encrypt(password.encode(), extra["public_key"])
            print(f"RSA encrypted password: {encrypted_password}")
            return encrypted_password

        case "des":
            cipher = DES.new(extra["des_key"], DES.MODE_ECB)
            padded_password = pad(password.encode(), DES.block_size)
            encrypted_password = cipher.encrypt(padded_password)
            print(f"DES encrypted password: {encrypted_password}")
            return encrypted_password

        case "aes":
            cipher = AES.new(extra["aes_key"], AES.MODE_ECB)
            padded_password = pad(password.encode(), AES.block_size)
            encrypted_password = cipher.encrypt(padded_password)
            print(f"AES encrypted password: {encrypted_password}")
            return encrypted_password


def decryptPassword(method, encrypted_password, extra):
    match method:
        case "rsa":
            private_key = rsa.PrivateKey.load_pkcs1(extra["result"]["private_key"])
            decrypted_password = rsa.decrypt(encrypted_password, private_key)
            print(f"RSA decrypted password: {decrypted_password}")
            return decrypted_password.decode()

        case "des":
            cipher = DES.new(extra["result"]["des_key"], DES.MODE_ECB)
            decrypted_password = cipher.decrypt(encrypted_password)
            unpadded_password = unpad(decrypted_password, DES.block_size).decode()
            print(f"DES decrypted password: {decrypted_password}")
            return unpadded_password

        case "aes":
            cipher = AES.new(extra["result"]["aes_key"], AES.MODE_ECB)
            decrypted_password = cipher.decrypt(encrypted_password)
            unpadded_password = unpad(decrypted_password, AES.block_size).decode()
            print(f"AES decrypted password: {decrypted_password}")
            return unpadded_password


@app.route("/register", methods=["POST"])
def register():
    register_name = request.form["register-name"]
    register_username = request.form["register-username"]
    register_password = request.form["register-password"]

    # Check user registered or not
    sqlQuery = f"SELECT COUNT(*) FROM ( SELECT username FROM rsa WHERE username = '{register_username}' UNION ALL SELECT username FROM des WHERE username = '{register_username}' UNION ALL SELECT username FROM aes WHERE username = '{register_username}' ) AS combined_usernames;"
    mycursor.execute(sqlQuery)
    result = mycursor.fetchone()
    mydb.commit()

    if (result["COUNT(*)"] != 0):
        return jsonify({ "status": "warning", "message": "User already exists" })
    else:
        rsa_start = time.perf_counter()
        public_key, private_key = rsa.newkeys(1024)
        rsa_encrypted_password = encryptPassword("rsa", register_password, {"public_key": public_key})
        rsa_end = time.perf_counter()
        rsa_generation_time = float("{:.10f}".format(rsa_end - rsa_start))  # seconds
        # Convert public_key object to string
        public_key_str = public_key.save_pkcs1().decode("utf-8")
        private_key_str = private_key.save_pkcs1().decode("utf-8")

        sqlQuery = "INSERT INTO rsa (name, username, password, encrypted_password, public_key, private_key, generation_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        rsa_data = (register_name, register_username, register_password, rsa_encrypted_password, public_key_str, private_key_str, rsa_generation_time,)

        mycursor.execute(sqlQuery, rsa_data)

        mydb.commit()

        if mycursor.rowcount != 1:
            return jsonify({"status": "error", "message": "RSA: The encrypted password failed to be stored in the database",})

        des_start = time.perf_counter()
        des_key = get_random_bytes(8)
        des_encrypted_password = encryptPassword("des", register_password, {"des_key": des_key})
        des_end = time.perf_counter()
        des_generation_time = float("{:.10f}".format(des_end - des_start))
        sqlQuery = "INSERT INTO des (name, username, password, encrypted_password, des_key, generation_time) VALUES (%s, %s, %s, %s, %s, %s)"
        des_data = (register_name, register_username, register_password, des_encrypted_password, des_key, des_generation_time,)

        mycursor.execute(sqlQuery, des_data)

        mydb.commit()

        if mycursor.rowcount != 1:
            return jsonify({"status": "error", "message": "DES: The encrypted password failed to be stored in the database"})

        aes_start = time.perf_counter()
        aes_key = get_random_bytes(16)
        aes_encrypted_password = encryptPassword("aes", register_password, {"aes_key": aes_key})
        aes_end = time.perf_counter()
        aes_generation_time = float("{:.10f}".format(aes_end - aes_start))
        sqlQuery = "INSERT INTO aes (name, username, password, encrypted_password, aes_key, generation_time) VALUES (%s, %s, %s, %s, %s, %s)"
        aes_data = (register_name, register_username, register_password, aes_encrypted_password, aes_key, aes_generation_time,)

        mycursor.execute(sqlQuery, aes_data)

        mydb.commit()

        if mycursor.rowcount != 1:
            return jsonify({"status": "error", "message": "AES: The encrypted password failed to be stored in the database"})
        else:
            return jsonify({"status": "success", "message": "The encrypted password is successfully stored in the database."})


@app.route("/login", methods=["POST"])
def login():
    login_username = request.form["login-username"]
    login_password = request.form["login-password"]
    decryption_method = request.form["login-decryption-method"]

    sqlQuery = f"SELECT * FROM {decryption_method} WHERE username = '{login_username}'"

    mycursor.execute(sqlQuery)

    result = mycursor.fetchone()

    mydb.commit()

    if result is not None:
        decrypted_password = decryptPassword(decryption_method, result["encrypted_password"], {"result": result})

        if login_password == decrypted_password and decrypted_password == result["password"]:
            sqlQuery = f"UPDATE matching_result SET success_times = success_times + 1 WHERE method = '{decryption_method}'"
            mycursor.execute(sqlQuery)
            mydb.commit()
            if mycursor.rowcount == 1:
                return jsonify({"status": "success", "message": f"The password is correct ({decryption_method.upper()})"})
            else:
                return jsonify({"status": "error", "message": f"{decryption_method.upper()}: fail to save the matching result (Decryption success)"})
        elif decrypted_password != result["password"]:
            sqlQuery = f"UPDATE matching_result SET fail_times = fail_times + 1 WHERE method = '{decryption_method}'"
            mycursor.execute(sqlQuery)
            mydb.commit()
            if mycursor.rowcount == 1:
                return jsonify({"status": "error", "message": f"{decryption_method.upper()}: fail to decrypt the encrypted password"})
            else:
                return jsonify({"status": "error", "message": f"{decryption_method.upper()}: fail to save the matching result (Decryption fail)"})
        else:
            return jsonify({"status": "warning", "message": "The password is incorrect"})
    else:
        return jsonify({"status": "warning", "message": "User does not exist"})


if __name__ == "__main__":
    app.run(debug=True)
