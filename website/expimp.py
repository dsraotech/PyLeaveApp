import cx_Oracle
import subprocess

# Database connection details
meshuser=input("Enter RLY network/username ")
meshpassword=meshuser
meshdns='MESH'+meshuser


source_user = "SITE_NW_SKEL"
source_password = "SITE_NW_SKEL"
destination_user = meshuser
destination_password = meshpassword
#source_dsn = cx_Oracle.makedsn("192.168.0.165", 1521, service_name="mesh")
source_dsn = 'SER165'
try:
    descon = cx_Oracle.connect(user=meshuser, password=meshpassword, dsn=meshdns)
except Exception as e:
    raise Exception(f"Not able to connect DESTINATION Database Server {e}")
try:
    srccon = cx_Oracle.connect(user=source_user, password=source_password, dsn=source_dsn)
except Exception as e:
    raise Exception(f"Not able to connect SOURCE Database Server {e}")

# Export tables from source database
def export_tables():
    #tables_list = " ".join(tables)
    msql = "SELECT 'ASIGNAL'||dlno ASIG, 'DSIGNAL'||dlno dsig FROM rhsetup WHERE dlno <>0 ORDER BY 1"
    srccur = srccon.cursor()
    srccur.execute(msql)
    table=srccur.fetchall()
    mytable = " ".join([" ".join(map(str, row)) for row in table])
    mytable = mytable + " RHSETUP ASIGTYPES DSIGTYPES"
    print("Export STARTED.")
    exp_command = f"exp {source_user}/{source_password}@{source_dsn} file=expdat.dmp STATISTICS=NONE tables={mytable}"
    try:
        subprocess.run(exp_command, shell=True, check=True)
    except Exception as e:
         print(f"EXP command returns : {e}")
    print("Export COMPLETED.")

# Drop existing tables in destination database
def drop_tables():
    msql = "SELECT dlno FROM rhsetup WHERE dlno <>0 ORDER BY 1"
    srccur = srccon.cursor()
    descur = descon.cursor()
    srccur.execute(msql)
    records = srccur.fetchall()
    for table in records:
        try:
            descur.execute(f"DROP TABLE DSIGNAL{table[0]} CASCADE CONSTRAINTS PURGE")
            print(f"Dropped table {table[0]}.")
        except Exception as e:
                print(f"Error dropping DSIGNAL{table[0]} table: {e}")
        try:
            descur.execute(f"DROP TABLE ASIGNAL{table[0]} CASCADE CONSTRAINTS PURGE")
            print(f"Dropped table {table[0]}.")
        except Exception as e:
                print(f"Error dropping ASIGNAL{table[0]} table: {e}")

    try:
            descur.execute(f"DROP TABLE RHSETUP CASCADE CONSTRAINTS PURGE")
            descur.execute(f"DROP TABLE DSIGTYPES CASCADE CONSTRAINTS PURGE")
            descur.execute(f"DROP TABLE ASIGTYPES CASCADE CONSTRAINTS PURGE")
            print(f"Dropped table {table}.")
    except Exception as e:
                print(f"Error dropping table {table}: {e}")


# Import tables into destination database
def import_tables():
    imp_command = f"imp {destination_user}/{destination_password}@{meshdns} file=expdat.dmp FULL=Y"
    try:
        subprocess.run(imp_command, shell=True, check=True)
    except Exception as e:
         print(f"IMP command returns : {e}")
    print("Import completed.")

# Main function
def main():
    export_tables()
    drop_tables()
    import_tables()

if __name__ == "__main__":
    main()
