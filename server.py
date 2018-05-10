from xmlrpc.server import *
import hashlib,time
from types import FunctionType
from functools import wraps

tokens = {}
credentials_data = {'ubdussamad' : ['5544781558847ecc54e3b3c406ed1c0e',True] , #Dummy Credentials for
                    'makshuf' : ['ccee66ac39ce8f6f4f2c450679f90525',False]  }  #Client-Side Testing
host  =("192.168.1.102", 8000)
def wrapper(method):
    @wraps(method)
    def wrapped(*args, **kwrds):
        print("NotImplimented")
        #TODO Further pre method processing block
    return wrapped

class MetaClass(type):
    def __new__(meta, classname, bases, classDict):
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            if isinstance(attribute, FunctionType):
                # should replace it with a wrapped version
                attribute = wrapper(attribute)
            newClassDict[attributeName] = attribute
        return type.__new__(meta, classname, bases, newClassDict)


class utils:
    def __init__(self):
        self.key = 0x00000
        
    def login(self,usr,pwd):
        
        credentials = 1 if usr in credentials_data else None
        if credentials and hashlib.md5(pwd.encode('utf-8')).hexdigest() == credentials_data[usr][0] :
            
            token = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:7]
            tokens[token] = [time.time(),1 if credentials_data[usr][1] else 0]
            print( "Master Login!" if credentials_data[usr][1] else 'User_Login!')
            return token,time.ctime()
        else:
            print("Zero Login")
            return 'Bad Credentials'
        
    def check_token(self,token):
        '''
        Codes:
        * 1,1 - Token Valid and Admin
        * 1,0 - Token Valid but Non-Admin
        * 0,0 = Token Expired or Invalid and Non Admin/Admin 
        * NO AUTHORITY OF ADMIN IF ADMIN'S TOKEN EXPIRED
        '''

        if token in tokens:
            delta = time.time() - tokens[token][0] < 60 #1 Minute(s)
            if delta:
                if tokens[token][1]:
                    return 1,1
                return 1,0
            return 0,0
        else: return 0,0

    def doc(self):
        return doc
        
    def list_tokens(self,token):
        
        if all(self.check_token(token)):
            return(tokens)
        return("Acess Denied! Non-Eligible or Expired Token.")

doc = '''This is a XML-RPC based Client Server for general method calls with high efficiency and low hastle.
\n Copyright 2018 BachmanitY Inc.'''

server = SimpleXMLRPCServer(host)
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
    print("Shutting Down the server.")
