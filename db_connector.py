import mysql.connector
from mysql.connector import Error

def db_connection():
  connection = mysql.connector.connect(host = 'localhost',database = "bank_ltd", user = "root", password = "ef007")
  if connection.is_connected():
    db_Info = connection.get_server_info()
    # print("Stay Blessed! You're live on mysql server version: ", db_Info)
  return connection

def card_list():
  card_no_list = []
  sql_select_query = "select * from card_details;"
  try: 
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    # print(record)
    for row in record:
      card_no_list.append(row[0])
    # print("Total no of row effected : >>>   ", cursor.rowcount)
    return card_no_list

  except mysql.connector.Error as Error:
    print("failed to connect to my sql server!!!", Error)
  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()
      # print("MySql connection is closed.")

def verify_pin(u_c_no, user_pin):
  connection = db_connection()
  cursor = connection.cursor()
  sql_query = "select pin from bank_ltd.card_details where card_no = " + u_c_no
  cursor.execute(sql_query)
  pin = cursor.fetchone()
  print()
  # print(pin[0], user_pin)
  verified = False
  if str(user_pin) == str(pin[0]):
    verified = True
  else:
    verified = False
  # print(verified)
  return verified

def verify_card_status(u_c_no):
  connection = db_connection()
  cursor = connection.cursor()

    # select card_no from tablename where cardno = cardno

  sql_query = "select status from bank_ltd.card_details where card_no = " + u_c_no
  # print(sql_query)
  cursor.execute(sql_query)
  status = cursor.fetchone()
  status = status[0]
  if status == 2:
    return "Great, You've that access"   
  elif status == 1:
    return 'Yeup, your card is freezed. Please contact bank branch :('
  elif status == 0:
    return 'Sorry, your card is blocked. Please Visit bank branch :('

def user_card():
  connection = db_connection()
  cursor = connection.cursor()
  card_no = card_list()
  # print(card_no)

  u_c_no = input("Please Enter your card no : >>>  \n")
  if u_c_no in card_no:
    print("Valid Card.\nYeah! We got it. For security purpose,")
    count = 3

    while count >= 0:
      user_pin = input('Enter user pin: >>>  ')
      if verify_pin(u_c_no, user_pin):
        print('pin verified')
        status = verify_card_status(u_c_no)
        print(status)
        # print('ef007')
      else:
        print('Wrong Pin! please try again !!!')
      count -= 1
      
    else: 
      connection = db_connection()
      cursor = connection.cursor()
      sql_query = "update card_details set status=0 where card_no = " + u_c_no
      cursor.execute(sql_query)
      connection.commit()
      print('Card Blocked!\nPlease connect to bank')

  else:
    print('No card found. / Invalid Card  !!!\nWant to get a New Card! please contact me!   :)')


user_card()
