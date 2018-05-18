#!/usr/bin/env python3
from xmlrpc.server import *
import hashlib,time,json
from lib.decorator import *

tokens = {}


def credentials_data(write=False,credentials=[]):
    with open('credentials.json','r') as f_obj:
        current_data = json.load(f_obj)
    if write:
        with open('credentials.json','w') as f_obj:
            last_user_id = max([ current_data[usr][2] for usr in current_data])
            current_data[credentials[0]] = [hashlib.md5(credentials[1].encode('utf-8')).hexdigest(), False , last_user_id+1]
            json.dump(current_data,f_obj)
            return(0)
    return current_data
session_timeout = 100 #Second(s)
host  =("0.0.0.0", 8090)

def clear_token_cache():#This is a least effort solution to the garbage collector problem
    '''This method is to to called at every administrative method call'''
    redundant_tokens = []
    for token in tokens:
        if time.time() - tokens[token][1] < session_timeout:
            redundant_tokens.append(token)
    for i in redundant_tokens:
        del tokens[i]


@for_all_methods(my_decorator(clear_token_cache))
class utils(object):
    
    def __init__(self):
        self.key = 0x00000
        
    def login(self,usr,pwd):
        
        credentials = 1 if usr in credentials_data() else None
        if credentials and hashlib.md5(pwd.encode('utf-8')).hexdigest() == credentials_data()[usr][0] :
            
            token = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:7]
            tokens[token] = [time.time(),1 if credentials_data()[usr][1] else 0]
            print( "Master Login!" if credentials_data()[usr][1] else 'User_Login!')
            return token,time.ctime()
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
            return(tokens)
        return(1,"Acess Denied! Non-Eligible or Expired Token.")
    
    def methods(self):
        return [i for i in utils.__dict__ if not i.startswith('_')]

    def check_users(self,token):
        if all(self.check_token(token)):
            return(credentials_data())
        return(1,"Acess Denied! Non-Eligible or Expired Token.")
    def change_pwd(self,usr,pwd,new_pwd):
        credentials = 1 if usr in credentials_data() else None
        if credentials and hashlib.md5(pwd.encode('utf-8')).hexdigest() == credentials_data()[usr][0] :
            credentials_data(True,[usr,new_pwd])
            return('Your password was sucessfully updated.')
        return('Bad Credentials')

    def register(self,usr,pwd):
        if usr not in credentials_data():
            credentials_data(True,[usr,pwd])
            return "User %s Created, You may login using the given credentials."%(usr,)
        else:
            return "Username Already Exists, Please try a different username."
    
            

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
