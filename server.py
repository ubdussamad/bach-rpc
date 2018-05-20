#!/usr/bin/env python3
from xmlrpc.server import *
import time,os,json
from hashlib import md5
import hashlib
try:
    from lib.decorator import *
except:
    from decorator import *
tokens = {}
session_timeout = 600 #Second(s)
host  =("0.0.0.0", 8090)


class data(object):
    def __init__(self):
        self.file = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))),os.path.join('data','asrar.txt'))

        if not os.path.exists(self.file):
            directory = os.path.dirname(self.file)
            if not os.path.exists(directory):
                os.mkdir(directory)
            with open(self.file,'w') as f_obj:
                    f_obj.write('admin,81dc9bdb52d04dc20036dbd8313ed055,1,101\n')

        with open(self.file,'r') as f_obj:
            data = f_obj.read()
            data = [i for i in data.split('\n') if i]
            keys = [i.split(',')[0] for i in data]
            values = [i.split(',')[1:] for i in data]
            self.credentials = dict(zip(keys, values))

    def append(self,data):
        with open(self.file,'a') as f_obj:
            new_user_id = max([int(self.credentials[usr][2]) for usr in self.credentials])
            f_obj.write(','.join([data[0],md5(data[1].encode('utf-8')).hexdigest(),data[2],str(new_user_id+1),'\n']))
            return(0)
    def update(self,usr,pwd):
        raise NotImplementedError
    
    



def clear_token_cache():#This is a least effort solution to the garbage collector problem
    '''This method is to to called at every administrative method call *needs improvement'''
    redundant_tokens = []
    for token in tokens:
        print('time delta is: %f'%(time.time() - tokens[token][0],))
        print('session to: %d'%(session_timeout,))
        if time.time() - tokens[token][0] > session_timeout:
            redundant_tokens.append(token)
    for i in redundant_tokens:
        del tokens[i]

@for_all_methods(my_decorator(clear_token_cache))
class utils(object):
    
    def __init__(self):
        self.key = 0x00000
        
    def login(self,usr,pwd):
        credentials = data().credentials
        pre_user = 1 if usr in credentials else None
        if pre_user and hashlib.md5(pwd.encode('utf-8')).hexdigest() == credentials[usr][0] :
            
            token = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:7]
            tokens[token] = [time.time(),1 if credentials[usr][1] else 0]
            print( "Master Login!" if credentials[usr][1] else 'User_Login!')
            return 0,token,time.ctime()
        else:
            print("Zero Login")
            return 1,'Bad Credentials'

    def check_token(self,token):
        '''
        Codes:
        * 1,1 - Token Valid and Admin
        * 1,0 - Token Valid but Non-Admin
        * 0,0 = Token Expired or Invalid and Non Admin/Admin 
        * NO AUTHORITY OF ADMIN IF ADMIN'S TOKEN EXPIRED
        '''

        if token in tokens:
            delta = time.time() - tokens[token][0] < session_timeout
            if delta:
                if tokens[token][1]:
                    return 1,1
                return 1,0
            return 0,0
        else: return 0,0

    def logout(self,token):
        if token in tokens:
            del tokens[token]
            return 0,'Session Discarded.'
        return 1,'Non-Exsistance or Expired token.'

    def doc(self):
        return doc,tokens
        
    def list_tokens(self,token):
        
        if all(self.check_token(token)):
            return(0,tokens)
        return(1,"Acess Denied! Non-Eligible or Expired Token.")
    
    def methods(self):
        return [i for i in utils.__dict__ if not i.startswith('_')]

    def check_users(self,token):
        if all(self.check_token(token)):
            return(0,data().credentials)
        return(1,"Acess Denied! Non-Eligible or Expired Token.")
    def change_pwd(self,usr,pwd,new_pwd):
        credentials = 1 if usr in data().credentials else None
        if credentials and hashlib.md5(pwd.encode('utf-8')).hexdigest() == data().credentials[usr][0] :
            data().append([usr,new_pwd,str(data().credentials[usr][1])])
            return(0,'Your password was sucessfully updated.')
        return(1,'Bad Credentials')

    def register(self,usr,pwd,auth=0):
        if usr not in data().credentials:
            data().append([usr,pwd,auth])
            return 0,"User %s Created, You may login using the given credentials."%(usr,)
        else:
            return 1,"Username Already Exists, Please try a different username."
    
            

doc = '''This is a XML-RPC based Client Server for general method calls with high efficiency and low hastle.
\n Copyright 2018 BachmanitY Inc.'''

server = SimpleXMLRPCServer(host,allow_none=True)
DocXMLRPCServer.set_server_title(server,server_title='BachmanitY Inc. Servers')
DocXMLRPCServer.set_server_name(server,server_name='Client Server Network BachmanitY Inc.')
DocXMLRPCServer.set_server_documentation(server,server_documentation=doc)

print('Bach-RPC Server Running on host: %s and Port: %s'%host)
print('Logging is enabled , server started at: %s. \n'%(time.ctime(),))
print('Hit Ctrl + C anytime to hault the server.\n')
server.register_introspection_functions()
server.register_instance( utils() )

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Server Haulted.")
