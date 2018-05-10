from xmlrpclib import *

transport = Transport()
transport.user_agent = 'DeerdhPro2'

xmlrpc = ServerProxy('http://192.168.1.102:8000/',
                                  allow_none=True, transport=transport)
z = xmlrpc.login('qazwsxqazwsx')
