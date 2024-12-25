import cx_Oracle
import re

# Connection details for source and destination databases
Suser='SITE_NW_SKEL'
Duser=input("Enter Destination User ")
source_conn = cx_Oracle.connect(user=Suser, password=Suser, dsn='SER165')

destination_conn = cx_Oracle.connect(user=Duser, password=Duser, dsn='dsrdb')

source_cursor = source_conn.cursor()
destination_cursor = destination_conn.cursor()
errddl=[]
errins=[]
wfile = open(r'c:\tmp\output.file','w')
# List of tables to be copied
source_cursor.execute("SELECT tname from TAB")
tables = source_cursor.fetchall()
for table in tables:
    # Fetch the table structure from the source database
    #table_name=table[0]
    table_name=table[0]
    mysql = f"SELECT DBMS_METADATA.GET_DDL('TABLE', '{table_name}') FROM dual"
    source_cursor.execute(mysql)
   
    #table_ddl = source_cursor.fetchone()
   
    table_ddl = source_cursor.fetchone()[0].read()
    # to remove user name in the create table
    table_ddl = re.sub(r'CREATE\s+TABLE\s+"[^"]+"\."[^"]+"\s*', f'CREATE TABLE {table_name} ', table_ddl, flags=re.IGNORECASE)
    # to remove all double quotes
    table_ddl = re.sub(r'"', f'', table_ddl, flags=re.IGNORECASE)
    # To get only core table description part
    pattern = r'CREATE TABLE\s+\w+\s*\((?:[^()]*|\((?:[^()]*|\([^()]*\))*\))*\)'

# Extract the core table definition
    match = re.search(pattern, table_ddl, re.DOTALL | re.IGNORECASE)
    table_ddl = match.group(0).strip()
    # Drop the table in the destination database if it exists
    oldtable = table_name+'OLD'
    # Copy destination data in to text file
    try:
        # TAKING destination table structure
        mysql = f"SELECT DBMS_METADATA.GET_DDL('TABLE', '{table_name}') FROM dual"
        destination_cursor.execute(mysql)
   
        #table_ddl = destination_cursor.fetchone()
   
        dtable_ddl = destination_cursor.fetchone()[0].read()
        # to remove user name in the create table
        dtable_ddl = re.sub(r'CREATE\s+TABLE\s+"[^"]+"\."[^"]+"\s*', f'CREATE TABLE {table_name} ', dtable_ddl, flags=re.IGNORECASE)
        # to remove all double quotes
        dtable_ddl = re.sub(r'"', f'', dtable_ddl, flags=re.IGNORECASE)
        # To get only core table description part
        dpattern = r'CREATE TABLE\s+\w+\s*\((?:[^()]*|\((?:[^()]*|\([^()]*\))*\))*\)'

        # Extract the core table definition
        dmatch = re.search(dpattern, dtable_ddl, re.DOTALL | re.IGNORECASE)
        dtable_ddl = match.group(0).strip()
        wfile.write(dtable_ddl+' --ENDTABLE\n')
        # END OF structure copy
        destination_cursor.execute(f"SELECT * FROM {table_name}")
        rows = destination_cursor.fetchall()
        column_names = [col[0] for col in destination_cursor.description]
        for row in rows:
            cleaned_row = ['' if item is None else str(item) for item in row]
            wfile.write('~'.join(cleaned_row) + '\n')
    except Exception as e:
        # Ignore when destination table not exist
        pass
    try:
        destination_cursor.execute(f"DROP TABLE {table_name} PURGE")
        #destination_conn.commit()
    except Exception as e:
        print(f"Error dropping {Duser} table {table_name}: {e}")

    # Create the table in the destination database using the DDL from the source
    try:
        destination_cursor.execute(table_ddl)
        #destination_conn.commit()
    except cx_Oracle.DatabaseError as e:
        errddl.append(table_name)
        print(f"Error creating {Duser} table {table_name}: {e}")

    # Fetch data from the source table
    source_cursor.execute(f"SELECT * FROM {table_name}")
    rows = source_cursor.fetchall()
    columns = [col[0] for col in source_cursor.description]

    # Insert data into the destination table
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join([':' + str(i+1) for i in range(len(columns))])})"
    try:
        destination_cursor.executemany(insert_query, rows)
        destination_conn.commit()
    except cx_Oracle.DatabaseError as e:
        errins.append(table_name)
        print(f"Error inserting data into {Duser} table {table_name}: {e}")

# Close the cursors and connections
source_cursor.close()
source_conn.close()
destination_cursor.close()
destination_conn.close()
if len(errins) >0 :
    print(f"Errors table during Insersion {errins}")
if len(errddl) >0 :
    print(f"Errors table during Insersion {errddl}")
