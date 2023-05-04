import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = os.getenv('DATABASE_PASSWORD'),
)

#prepare cursor obj

cursorObject = dataBase.cursor()

#create DB

cursorObject.execute("CREATE DATABASE trackflowDB")

print("i worked!")