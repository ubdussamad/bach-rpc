from xmlrpc.client import *

transport = Transport()
transport.user_agent = 'DeerdhPro2'
import random
xmlrpc = ServerProxy('http://0.0.0.0:8090/',
                                  allow_none=True, transport=transport)
token = 0
try:
    a = xmlrpc.login('admin','1234')
    if not a[0]:
        print("Login test: Pass!")
        token = str(a[1])
    else: raise
except Exception as err:
    print("Login test: Fail5!",err)

try:
    b = xmlrpc.change_pwd('admin','1234','1234')
    if not b[0]: print("Change key: Pass!")
    else: raise
except Exception as err:
    print("Change key: Fail!")
    print(err)

try:
    j = lambda: [random.randint(97,122) for i in range(8)]
    test_usr,pwd = 'test_'+''.join([chr(i) for i in j()]),''.join([chr(i) for i in j()])
    c = xmlrpc.register(test_usr,pwd)
    if not c[0]:
        print('Resgister user: Pass!')
    else:
        raise
except Exception as err:
    print('Resgister user: Fail!',err)

try:
    if all(xmlrpc.check_token(token)):print("Check Token: Pass!")
    else:raise
except:
    print('Check token: Fail!')

try:
    if not xmlrpc.list_tokens(token)[0]:print("List Token: Pass!")
    else:raise
except:
    print('List token: Fail!')

try:
    if not xmlrpc.check_users(token)[0]:print("Check Users: Pass!")
    else:raise
except:
    print('Check Users: Fail!')
