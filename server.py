#!/usr/bin/env python3
from xmlrpc.server import *
import time,os,json
from hashlib import md5
from lib.decorator import *



session_timeout = 600 #Second(s)
host  =("0.0.0.0", 8090)

def hexmd5(x):
    return md5(str(x).encode('utf-8')).hexdigest()

class data(object):

    def __init__(self):
        ''' Class for Reading/Writing/Appending to the
            credentials data. '''
        self.file = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))),os.path.join('data','asrar.txt'))

        if not os.path.exists(self.file):
            directory = os.path.dirname(self.file)
            if not os.path.exists(directory):
                os.mkdir(directory)
            with open(self.file,'w') as f_obj:
                    usr = input('Setup admin username and password for the given server: \n\n Enter Username:')
                    pwd = input('\n Enter Password:')
                    f_obj.write(','.join([ usr if usr else 'admin' , hexmd5(pwd) if pwd else hexmd5(1234) ,
                                  '1' , '101'])+'\n')
                    f_obj.close()
                    print('\nAdmin Sucessfully registered, Server is running....')

    def append(self,data):
        '''.append(self, [usrname,password , authentication]'''
        with open(self.file,'a') as f_obj:
            new_user_id = max([int(self.peek()[usr][2]) for usr in self.peek()])
            f_obj.write(','.join([data[0],hexmd5(data[1]),str(data[2]),str(new_user_id+1),'\n']))
            f_obj.close()
        return(0)

    def update(self,data):
        '''.append(self, [usrname,new_password, authentication, user_id]'''
        assert len(data) == 4
        f_obj = open(self.file,'r')
        file = f_obj.readlines()
        f_obj.close()
        f_obj = open(self.file,'w')
        index = int(data[3])-101
        for i,j in enumerate(file):
            if i==index:
                f_obj.write(','.join(map(str,data))+'\n')
            else:
                f_obj.write(j)
        f_obj.close()
        return([0])

    def peek(self):
        with open(self.file,'r') as f_obj:
            data = f_obj.read()
            data = [[j for j in i.split(',') if j] for i in data.split('\n') if i]
            self.cred_dict = dict([(i[0],i[1:]) for i in data])
            f_obj.close()
        return self.cred_dict
    
    


class utils(object):
    
    def __init__(self):
        self.key = 0x00000
        self.credentials = data()
        self.__tokens = {} #Tokens are stored in volatile memory as to log everyone out at server shutdown.

    def clear_token_cache(self,user_id=''):
        '''Removes Expired Tokens from the memory and also removed pre-exsistant tokens of a user.'''
        if user_id:
            temp_token_list = self.__tokens.copy()
            for token in temp_token_list:
                if temp_token_list[token][2] == user_id:
                    del self.__tokens[token]
            return(0)

        redundant_tokens = []
        for token in tokens:
            if time.time() - tokens[token][0] > session_timeout:
                redundant_tokens.append(token)
        for i in redundant_tokens:
            del tokens[i]
            
    def login(self,usr,pwd):
        temp = self.credentials.peek()
        pre_user = 1 if usr in temp else None
        
        if pre_user and hexmd5(pwd) == temp[usr][0] :
            
            token = hexmd5(time.time())[:7]
            self.clear_token_cache(temp[usr][2]) #Last generated Token of the user will be cleared (If Valid)
            self.__tokens[token] = [time.time(),1 if temp[usr][1] else 0,temp[usr][2]]
            print( "Master Login!" if temp[usr][1] else '')
            return 0,token,time.ctime()
        else:
            return 1,'Bad Credentials or Non-Exsistant User'

    def check_token(self,token):
        '''
        Codes:
        * 1,1 - Token Valid and Admin
        * 1,0 - Token Valid but Non-Admin
        * 0,0 = Token Expired or Invalid and Non Admin/Admin 
        * NO AUTHORITY OF ADMIN IF ADMIN'S TOKEN EXPIRED
        '''

        if token in self.__tokens:
            delta = time.time() - self.__tokens[token][0] < session_timeout
            if delta:
                if self.__tokens[token][1]:
                    return 1,1
                return 1,0
            return 0,0
        else: return 0,0

    def logout(self,token):
        if token in self.__tokens:
            del self.__tokens[token]
            return 0,'Session Discarded.'
        return 1,'Non-Exsistance or Expired token.'

    def doc(self):
        return doc
        
    def methods(self):
        return [i for i in utils.__dict__ if not i.startswith('_')]

    def admin(self,token,option,data=[]):
        ''' rpc.admin( self , token , option= des/lo/lu/lt/ls , data =[optional incase of des])
            data consists of [ username, pwd , auth , usr_id ]
            --> pwd in data must be hashed when modified
            options:
                * des - Designate a user to admin or vice-versa
                * lo  - List Online Users
                * lu  - List all  the users
                * lt  - List all the current token
                * ls  - List all available options    '''
        if not all(self.check_token(token)):
            return(1,'Denied!!')
        if option=='des':
            self.credentials.update( data )
        elif option=='lo':
            return self.__list_online_users()
        elif option == 'lu':
            return self.__list_users()
        elif option=='lt':
            return self.__list_tokens()
        elif option == 'ls':
            return self.admin.__doc__
        else:
            return(1,'Bad Option.')
    
    def change_pwd(self,usr,pwd,new_pwd):
        credentials = 1 if usr in self.credentials.peek() else None
        if credentials and hexmd5(pwd) == self.credentials.peek()[usr][0] :
            self.credentials.update(  [usr,hexmd5(new_pwd)]+self.credentials.peek()[usr][1:] )
            return(0,'Your password was sucessfully updated.')
        return(1,'Bad Credentials')

    def register(self,usr,pwd,auth=0):
        if usr not in self.credentials.peek():
            self.credentials.append([usr,pwd,auth])
            return 0,"User %s Created, You may login using the given credentials."%(usr,)
        else:
            return 1,"Username Already Exists, Please try a different username."

    def __list_online_users(self):
        online_users = []
        for i in self.__tokens:
            for j in self.credentials.peek():
                if self.__tokens[i][2] == self.credentials.peek()[j][2] and  time.time() - self.__tokens[i][0] < session_timeout:
                    online_users.append(j)
        return(online_users)

    def __list_users(self):
        return(0,self.credentials.peek())

    def __list_tokens(self):
        return(0,self.__tokens)
    
            

doc = '''This is a XML-RPC based Client Server for general method calls with high efficiency and low hastle.
\n Copyright 2018 BachmanitY Inc.'''

server = SimpleXMLRPCServer(host,allow_none=True)
DocXMLRPCServer.set_server_title(server,server_title='BachmanitY Inc. Servers')
DocXMLRPCServer.set_server_name(server,server_name='Client Server Network BachmanitY Inc.')
DocXMLRPCServer.set_server_documentation(server,server_documentation=doc)

print('Bach-RPC Server Running on host: %s and Port: %s'%host)
print('Server State: Solid  Node Status: Unimplimented')
print('Logging is enabled , server started at: %s. \n'%(time.ctime(),))
print('Hit Ctrl + C anytime to hault the server.\n')
server.register_introspection_functions()
server.register_instance( utils() )

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Server Haulted.")
