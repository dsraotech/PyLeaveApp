# pyinstaller --onefile <pyfile>
import cx_Oracle
import sys

def rly_data_dump(networkname):
    msql=''
    try:
        # Connection details
        #dsn_tns = cx_Oracle.makedsn('192.168.0.165', '1521', service_name='mesh')
        connection = cx_Oracle.connect(user='ONEMESH', password='ONEMESH', dsn='SER165')
        cursor = connection.cursor()


        # Get database link
        cursor.execute("""
            SELECT db_link 
            FROM dba_db_links 
            WHERE UPPER(username)=UPPER(:Networkname)
        """, Networkname=networkname)
        
        mdb_link = cursor.fetchone()[0]
        #table_name="TTT1"
        #msql=f"begin dbms_utility.exec_ddl_statement@{mdb_link}('drop table {table_name}'); end;";
        #cursor.execute(msql)
   # Drop all tables in SITE_NW_SKEL schema USING dblink
        cursor.execute(f"""
            SELECT dlno FROM SITE_NW_SKEL.rhsetup
            WHERE dlno<>0 ORDER BY dlno""")
        print('Dropping existing tables')
        dlnos = cursor.fetchall()
        for dlno in dlnos:
            try:
                msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('DROP TABLE ASIGNAL{dlno[0]} PURGE'); END;"
                cursor.execute(msql)
            except Exception as e:
                error, = e.args
                if error.code != 942:
                    raise Exception(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}\nSQL: {msql}")
            try:
                msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('DROP TABLE DSIGNAL{dlno[0]} PURGE'); END;"
                cursor.execute(msql)
            except Exception as e:
                error, = e.args
                if error.code != 942:
                    raise Exception(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}\nSQL: {msql}")
        
        # Dropping Other tables rhsetup, dsigtypes, asigtypes'

        try:
            msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('DROP TABLE display_network PURGE'); END;"
            cursor.execute(msql)
        except Exception as e:
                error, = e.args
                if error.code != 942:
                    raise Exception(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}\nSQL: {msql}")

        try:
            msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('DROP TABLE rhsetup PURGE'); END;"
            cursor.execute(msql)
        except Exception as e:
                error, = e.args
                if error.code != 942:
                    raise Exception(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}\nSQL: {msql}")

        try:
            msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('DROP TABLE dsigtypes PURGE'); END;"
            cursor.execute(msql)
        except Exception as e:
                error, = e.args
                if error.code != 942:
                    raise Exception(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}\nSQL: {msql}")

        try:
            msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('DROP TABLE asigtypes PURGE'); END;"
            cursor.execute(msql)
        except Exception as e:
                error, = e.args
                if error.code != 942:
                    raise Exception(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}\nSQL: {msql}")

        print('Creating RHSETUP table')
        # Create display_network table
        msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('CREATE TABLE display_network AS SELECT \''{networkname}\'' network, \''In Progress\'' status FROM dual'); END;"
        #msql = f"CREATE TABLE display_network@{mdb_link} AS SELECT \'{networkname}\' network, \'In Progress\' status FROM dual"
        cursor.execute(msql)

        # Create RHSETUP table
        msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('CREATE TABLE RHSETUP AS SELECT * FROM SITE_NW_SKEL.rhsetup'); END;"
        cursor.execute(msql)

        print('Creating DSIGTYPES table')
        # Create DSIGTYPES table
        msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('CREATE TABLE DSIGTYPES AS SELECT * FROM SITE_NW_SKEL.DSIGTYPES'); END;"
        cursor.execute(msql)

        print('Creating ASIGTYPES table')
        # Create ASIGTYPES table
        msql = f"BEGIN dbms_utility.exec_ddl_statement@{mdb_link}('CREATE TABLE ASIGTYPES AS SELECT * FROM SITE_NW_SKEL.ASIGTYPES'); END;"
        cursor.execute(msql)

        print('Creating DSIGNAL and ASIGNAL tables')
        # Create DSIGNAL and ASIGNAL tables for each dlno
        cursor.execute("SELECT dlno FROM SITE_NW_SKEL.RHSETUP WHERE dlno<>0 ORDER BY 1")
        dlnos = cursor.fetchall()
        for dlno in dlnos:
            dlno = dlno[0]
            print(f"creating DSIGNAL{dlno}",end='\r', flush=True)
            msql = f"CREATE TABLE DSIGNAL{dlno}@{mdb_link} AS SELECT * FROM SITE_NW_SKEL.DSIGNAL{dlno} "
            cursor.execute(msql)
            print(f"creating ASIGNAL{dlno}",end='\r', flush=True)
            msql = f"CREATE TABLE ASIGNAL{dlno}@{mdb_link} AS SELECT * FROM SITE_NW_SKEL.ASIGNAL{dlno}"
            cursor.execute(msql)

        # Commit the transaction
        msql = f"UPDATE display_network@{mdb_link} SET status=\'Successfull\'"
        cursor.execute(msql)
        connection.commit()

    except Exception as e:
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
        print("Usage: Parameter of network name is missing")
        #sys.exit(1)
    else:
        networkname = sys.argv[1]
    networkname='SCOTT'
    rly_data_dump(networkname)
