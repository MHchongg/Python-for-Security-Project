import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", password="", database="python_user"
)

mycursor = mydb.cursor(dictionary=True)

if __name__ == "__main__":
    sqlQuery = "SELECT AVG(rsa.generation_time) AS RSA_AVG_GENERATION_TIME, AVG(des.generation_time) AS DES_AVG_GENERATION_TIME, AVG(aes.generation_time) AS AES_AVG_GENERATION_TIME FROM rsa, des, aes;"
    mycursor.execute(sqlQuery)
    result = mycursor.fetchone()
    mydb.commit()

    print(result)
