import cx_Oracle
import getpass

# Database connection parameters
dsn_tns = cx_Oracle.makedsn('192.168.0.80', 1521, service_name='oracle')  # e.g., 'localhost', '1521', 'orclpdb1'
connection = cx_Oracle.connect(user='SYS', password='MncCti_3710', dsn=dsn_tns, mode=cx_Oracle.SYSDBA)
remarks=''
# Function to get user input and insert into the database
def capture_and_insert():
    # Capture input from the user
    print('')
    ip_address = input("Enter IP address / AD name                  : ").upper()
    if len(ip_address) > 100:
        print("IP address / AD name should not exceed 100 characters.")
        return

    user_type = input("Enter USER type (USER or SERVER)            : ").upper()
    if user_type not in ['USER', 'SERVER']:
        print("USER type should be either 'USER' or 'SERVER'.")
        return
    if user_type=='USER':
            remarks='PC'
    else:
            remarks='Server'
    username = input("Enter DB username (eg. TAMS, CASHFLOWUSER)  : ").upper()
    if len(username) > 30:
        print("Username should not exceed 30 characters.")
        return
    print('')
    yesno = input("Save Data (Y/N)                             : ").upper()
    if yesno != 'Y':
       return
    # Insert data into the database
    try:
        cursor = connection.cursor()
        sql_insert = """INSERT INTO ipad_base_access  VALUES (:ip_address, :user_type, :username,1,:remarks,sysdate)"""
        cursor.execute(sql_insert, [ip_address, user_type, username,remarks])
        connection.commit()
        print('')
        print("Data inserted successfully.")
    except cx_Oracle.DatabaseError as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

# Capture and insert data
while 1==1:
    capture_and_insert()
    print('')
    cont = input("Do you want to add another (Y/N) :  ").upper()
    if cont=='Y':
        pass
    else:
        break
# Close the connection
connection.close()
