from xmlrpc.client import *

transport = Transport()
transport.user_agent = 'DeerdhPro2'

xmlrpc = ServerProxy('http://localhost:8090/',
                                  allow_none=True, transport=transport)

