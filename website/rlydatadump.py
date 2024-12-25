# pyinstaller --onefile <pyfile>
import cx_Oracle
import sys

def rly_data_dump(networkname):
    try:
        # Connection details
        dsn_tns = cx_Oracle.makedsn('192.168.0.165', '1521', service_name='mesh')
        connection = cx_Oracle.connect(user='ONEMESH', password='ONEMESH', dsn=dsn_tns)
        cursor = connection.cursor()

        # Drop all tables in SITE_NW_SKEL schema
        cursor.execute("""
            SELECT OBJECT_NAME 
            FROM DBA_OBJECTS 
            WHERE owner='SITE_NW_SKEL' and object_type='TABLE'
        """)
        print('Dropping existing tables')
        tables = cursor.fetchall()
        for table in tables:
            tname = table[0]
            msql = f"DROP TABLE SITE_NW_SKEL.{tname} PURGE"
            cursor.execute(msql)
        
        # Get database link
        cursor.execute("""
            SELECT db_link 
            INTO :mdb_link 
            FROM dba_db_links 
            WHERE UPPER(username)=UPPER(:networkname)
        """, networkname=networkname)
        
        mdb_link = cursor.fetchone()[0]

        print('Creating RHSETUP table')
        # Create display_network table
        msql = f"CREATE TABLE SITE_NW_SKEL.display_network AS SELECT \'{networkname}\' network, \'In Progress\' status FROM dual"
        cursor.execute(msql)

        # Create RHSETUP table
        msql = f"CREATE TABLE SITE_NW_SKEL.RHSETUP AS SELECT * FROM rhsetup@{mdb_link}"
        cursor.execute(msql)

        print('Creating DSIGTYPES table')
        # Create DSIGTYPES table
        msql = f"CREATE TABLE SITE_NW_SKEL.DSIGTYPES AS SELECT * FROM DSIGTYPES@{mdb_link}"
        cursor.execute(msql)

        print('Creating ASIGTYPES table')
        # Create ASIGTYPES table
        msql = f"CREATE TABLE SITE_NW_SKEL.ASIGTYPES AS SELECT * FROM ASIGTYPES@{mdb_link}"
        cursor.execute(msql)

        print('Creating DSIGNAL and ASIGNAL tables')
        # Create DSIGNAL and ASIGNAL tables for each dlno
        cursor.execute("SELECT dlno FROM SITE_NW_SKEL.RHSETUP WHERE dlno<>0 ORDER BY 1")
        dlnos = cursor.fetchall()
        for dlno in dlnos:
            dlno = dlno[0]
            print(f"creating DSIGNAL{dlno}",end='\r', flush=True)
            msql = f"CREATE TABLE SITE_NW_SKEL.DSIGNAL{dlno} AS SELECT * FROM DSIGNAL{dlno}@{mdb_link}"
            cursor.execute(msql)
            print(f"creating ASIGNAL{dlno}",end='\r', flush=True)
            msql = f"CREATE TABLE SITE_NW_SKEL.ASIGNAL{dlno} AS SELECT * FROM ASIGNAL{dlno}@{mdb_link}"
            cursor.execute(msql)

        # Commit the transaction
        msql = f"UPDATE SITE_NW_SKEL.display_network SET status=\'Successfull\'"
        cursor.execute(msql)
        connection.commit()

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        raise Exception(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}\nSQL: {msql}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        print(f"SUCCESSFULLY created tables for {networkname} Network")

if __name__ == "__main__":
    arg_length = len(sys.argv)
    if arg_length != 2:
        print("Usage: python script_name.py networkname")
        sys.exit(1)
    
    networkname = sys.argv[1]
    #networkname='PALASA'
    rly_data_dump(networkname)
