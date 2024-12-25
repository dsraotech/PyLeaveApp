from pyad import *
pyad.set_defaults(ldap_server="PDC.EFFTRONICS.LOCAL",username="dsubbarao",password="Dsrao@111")
user=pyad.aduser.ADUser.from_cn("dspurthi")
myname=user.get_attribute("whencreated")
print(myname)