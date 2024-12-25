import os
import cx_Oracle
import csv
from datetime import datetime
import sys

# parameters 
arg_length = len(sys.argv)
param0 = sys.argv[0]
if arg_length==2:
   param1 = sys.argv[1]
else:
   param1 = r"D:\27.Extract DB Tool\demo\DAT'\SGRDJSPL_DIGDATA94_31MAR24"

# Oracle database connection parameters
dsn = cx_Oracle.makedsn("192.168.15.52", "1521", service_name="dsrdb")
connection = cx_Oracle.connect(user="SCOTT", password="SCOTT", dsn=dsn)

def get_dat_files(directory):
    try:
        files = os.listdir(directory)
        #print(f"Files in directory '{directory}': {files}")  # Debugging statement
        dat_files = [f for f in files if f.endswith('.DAT')]
        #print(f".dat files: {dat_files}")  # Debugging statement
        return dat_files
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
        return []

def extract_table_name(filename):
    parts = filename.split('_')
    print(f" split data {parts}")
    return parts[1]

def insert_data_into_table(table_name, data):
    print(f"Writing into the table {table_name}")
    cursor = connection.cursor()
    #placeholders = ', '.join([':' + str(i+1) for i in range(len(data[0]))])
    #sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
    #sql = f"INSERT INTO {table_name} VALUES ({', '.join([placeholders[:-1] + f', TO_DATE(:{len(data[0])}, \'DD-MON-YYYY HH24:MI:SS\')'])})"
    date_indices = [i for i, value in enumerate(data[0]) if is_date_string(value)]
    columns = ', '.join([
        f"TO_DATE(:{i+1}, 'DD-MON-YYYY HH24:MI:SS')" if i in date_indices else f":{i+1}"
        for i in range(len(data[0]))
    ])
    sql = f"INSERT INTO {table_name} VALUES ({columns})"
    for row in data:
        #converted_row = [convert_to_oracle_date(col) for col in row]
        cursor.execute(sql, row)
        
    connection.commit()
    cursor.close()

def process_files(directory):
    dat_files = get_dat_files(directory)
    for filename in dat_files:
        table_name = extract_table_name(filename)
        if table_name:
            file_path = os.path.join(directory, filename)
            try:
                print(f"Reading text file {filename}")
                with open(file_path, 'r', newline='') as file:
                    reader = csv.reader(file, delimiter='~')
                    first_row = next(reader)
                    if first_row[0] == 'SEPARATOR:':
                       data = list(reader)
                    else:
                      reader = csv.reader(file, delimiter='~')
                      data = [first_row]+list(reader)
                    insert_data_into_table(table_name, data)
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")

def is_date_string(s):
    try:
        datetime.strptime(s, '%d-%b-%Y %H:%M:%S')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    directory = rf"{param1}"
    process_files(directory)
    connection.close()
