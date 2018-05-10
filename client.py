from xmlrpc.client import *

transport = Transport()
transport.user_agent = 'DeerdhPro2'

xmlrpc = ServerProxy('http://localhost:8000/',
                                  allow_none=True, transport=transport)

