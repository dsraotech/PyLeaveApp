import ldap3
from ldap3.core.exceptions import LDAPException, LDAPBindError
import logging

logging.basicConfig(level=logging.DEBUG)

LDAP_HOST = 'ldap://192.168.0.9'
LDAP_BIND_USER = 'cn=dsubbarao,DC=EFFTRONICS,DC=LOCAL'
LDAP_BIND_PASSWORD = 'Dsrao@111'

logging.debug(f"LDAP Host: {LDAP_HOST}")
logging.debug(f"LDAP Bind User: {LDAP_BIND_USER}")

server = ldap3.Server(LDAP_HOST, get_info=ldap3.ALL)

try:
    conn = ldap3.Connection(
        server,
        user=LDAP_BIND_USER,
        password=LDAP_BIND_PASSWORD,
        auto_bind=True
    )
    print("Bind successful.")
except LDAPBindError as e:
    logging.error(f"LDAP bind error: {e}")
except LDAPException as e:
    logging.error(f"LDAP error: {e}")
