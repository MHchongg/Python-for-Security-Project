from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import rsa
import time

app = Flask(__name__)
CORS(app)

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="python_user")

mycursor = mydb.cursor(dictionary=True)

def encryptPassword(method, password, extra):
    match method:
        case "rsa":
            encrypted_password = rsa.encrypt(password.encode(), extra["public_key"])
            return encrypted_password

        case 'des':
            print('des encrypt')

        case 'aes':
            print('aes encrypt')


def decryptPassword(method, encrypted_password, extra):
    match method:
        case "rsa":
            plaintext_password = rsa.decrypt(encrypted_password, extra["private_key"])
            return plaintext_password.decode()
        
        case "des":
            print("des decrypt")

        case "aes":
            print("aes decrypt")


@app.route("/register", methods=["POST"])
def register():
    register_name = request.form["register-name"]
    register_username = request.form["register-username"]
    register_password = request.form["register-password"]

    rsa_start = time.time()
    public_key, private_key = rsa.newkeys(1024)
    encrypted_password = encryptPassword('rsa', register_password, { "public_key": public_key })
    rsa_end = time.time()
    rsa_generation_time = rsa_end - rsa_start #seconds
    # Convert public_key object to string
    public_key_str = public_key.save_pkcs1().decode('utf-8')
    private_key_str = private_key.save_pkcs1().decode('utf-8')

    sqlQuery = "INSERT INTO rsa (name, username, password, encrypted_password, public_key, private_key, generation_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (register_name, register_username, register_password, encrypted_password, public_key_str, private_key_str, rsa_generation_time)

    mycursor.execute(sqlQuery, data)

    mydb.commit()

    if (mycursor.rowcount != 1):
        return jsonify({ "status": "fail"})
    else:
        return jsonify({ "status": "success" })


@app.route("/login", methods=["POST"])
def login():
    login_username = request.form["login-username"]
    login_password = request.form["login-password"]

    sqlQuery = "SELECT * FROM rsa WHERE username = %s"

    mycursor.execute(sqlQuery, (login_username, ))

    result = mycursor.fetchone()

    mydb.commit()

    private_key = rsa.PrivateKey.load_pkcs1(result["private_key"])

    plaintext_password = decryptPassword('rsa', result["encrypted_password"], { "private_key": private_key })

    if (login_password == plaintext_password):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})


if __name__ == "__main__":
    app.run(debug=True)
