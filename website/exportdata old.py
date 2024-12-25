import cx_Oracle
import os

def check_tnsname_exists(tnsname):
    try:
        cx_Oracle.makedsn(tnsname, 1521)
        return True
    except:
        return False

def read_division_file_and_display(destination_conn):
    cursor = destination_conn.cursor()
    cursor.execute("SELECT division_name, division_code, network_name FROM division_file")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Division Name: {row[0]}, Division Code: {row[1]}, Network Name: {row[2]}")
    cursor.close()

def confirm_transfer():
    while True:
        confirmation = input("Do you want to proceed with the data transfer? (yes/no): ").strip().lower()
        if confirmation in ['yes', 'no']:
            return confirmation == 'yes'

def transfer_data(source_conn, destination_conn):
    source_cursor = source_conn.cursor()
    destination_cursor = destination_conn.cursor()

    source_cursor.execute("SELECT table_name FROM user_tables")
    tables = source_cursor.fetchall()

    for table in tables:
        table_name = table[0]
        
        try:
            destination_cursor.execute(f"DROP TABLE {table_name}")
        except cx_Oracle.DatabaseError as e:
            print(f"Error dropping table {table_name}: {e}")

        source_cursor.execute(f"SELECT * FROM {table_name}")
        rows = source_cursor.fetchall()
        column_names = [row[0] for row in source_cursor.description]
        column_names_str = ", ".join(column_names)
        column_placeholders = ", ".join([":" + str(i+1) for i in range(len(column_names))])

        create_table_query = f"CREATE TABLE {table_name} AS SELECT * FROM {table_name} WHERE 1=0"
        destination_cursor.execute(create_table_query)
        insert_query = f"INSERT INTO {table_name} ({column_names_str}) VALUES ({column_placeholders})"
        destination_cursor.executemany(insert_query, rows)
        destination_conn.commit()
        print(f"Data transferred successfully for table {table_name}")

    source_cursor.close()
    destination_cursor.close()

def main():
    source_dsn = input("Enter the TNSNAME for the source database: ").strip()
    destination_tns = input("Enter the TNSNAME for the destination database: ").strip()

    if not check_tnsname_exists(destination_tns):
        print(f"TNSNAME '{destination_tns}' does not exist in the source database.")
        return

    source_username = input("Enter the source database username: ").strip()
    source_password = input("Enter the source database password: ").strip()
    destination_username = input("Enter the destination database username: ").strip()
    destination_password = input("Enter the destination database password: ").strip()

    try:
        source_conn = cx_Oracle.connect(source_username, source_password, source_dsn)
        destination_conn = cx_Oracle.connect(destination_username, destination_password, destination_tns)

        read_division_file_and_display(destination_conn)

        if confirm_transfer():
            transfer_data(source_conn, destination_conn)
        else:
            print("Data transfer aborted by user.")

    except cx_Oracle.DatabaseError as e:
        print(f"Database connection error: {e}")

    finally:
        if 'source_conn' in locals() and source_conn:
            source_conn.close()
        if 'destination_conn' in locals() and destination_conn:
            destination_conn.close()

if __name__ == "__main__":
    main()
