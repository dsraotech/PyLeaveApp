from ldap3 import Server, Connection, SUBTREE

# LDAP Server Configuration
LDAP_HOST = 'ldap://EFFTRONICS.LOCAL'
LDAP_BIND_USER = 'cn=sms,DC=EFFTRONICS,DC=LOCAL'
LDAP_BIND_PASSWORD = 'Efftronics@123'
LDAP_BASE_DN = 'ou=users,DC=EFFTRONICS,DC=LOCAL'

# Establish connection to LDAP server
server = Server(LDAP_HOST)
conn = Connection(server, user=LDAP_BIND_USER, password=LDAP_BIND_PASSWORD, auto_bind=True)

# Search LDAP directory
conn.search(search_base=LDAP_BASE_DN,
            search_filter='(objectClass=person)',
            search_scope=SUBTREE,
            attributes=['cn', 'mail'])

# Print search results
for entry in conn.entries:
    print(f'CN: {entry.cn}, Email: {entry.mail}')

# Close connection
conn.unbind()
