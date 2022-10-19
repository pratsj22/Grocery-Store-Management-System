import datetime
import mysql.connector

con = None

def get_sql_connection():
  print("Opening mysql connection")
  global con

  if con is None:
    con = mysql.connector.connect(user='root', password='spider',host='127.0.0.1', port='3307', database='grocery store')

  return con