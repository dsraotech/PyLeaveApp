import cx_Oracle
from datetime import datetime

def is_date_string(s):
    try:
        datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
    
destination_conn = cx_Oracle.connect(user='SCOTT', password='SCOTT', dsn='dsrdb')
cursor=destination_conn.cursor()
endtable=False
firsttime=True
command=''
table_name=''
file=open(r'c:\tmp\output.file', 'r')  
myinput=input("Please enter T for Truncate table or D Drop table before insert : ")
if myinput not in ('D', 'T'):
    print("Invalid input. Exiting.")
    exit()

for line in file:
   if ('CREATE TABLE' in line ) or not endtable:
       endtable=False
       command="".join([command, line])
       
       if 'ENDTABLE' in line:  # to find end of the ddl statement
         destination_conn.commit()
         endtable=True
         firsttime=True
         try:
            lines=command.strip().split(' ')
            table_name=lines[2]
            print(f"data is getting inserted into the table {table_name}")
            try:  # P for drop and D for delete the table as per user input
              if myinput=='D':
                 mysql=f'DROP TABLE {table_name} PURGE'
                 cursor.execute(mysql)
              else:
                 mysql=f'DELETE {table_name}'
                 cursor.execute(mysql)
            except Exception as e:
                 pass
            if myinput=='D': # execute DDL if the user input is P
               cursor.execute(command)
         except Exception as e:
            pass # Ignore the errors
   else:
       if firsttime:
          firsttime=False
        #   lines=command.strip().split(' ')
        #   table_name=lines[2]
       command=''
       columns = line.strip().split('~')
       date_indices = [i for i, value in enumerate(columns) if is_date_string(value)]
       colstr = ', '.join([
        f"TO_DATE(:{i+1}, 'YYYY-MM-DD HH24:MI:SS')" if i in date_indices else f":{i+1}"
        for i in range(len(columns))])

       insert_query = f"INSERT INTO {table_name} VALUES ({colstr})"

       values = line.strip().split('~')
       try:
          cursor.execute(insert_query, values)
       except Exception as e:
          print(insert_query)
          print(values)

destination_conn.commit()
cursor.close()
destination_conn.close()
