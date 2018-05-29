#!/usr/bin/env python3
from xmlrpc.server import *
from lib.decorator import time_wrapper
from lib.user_mgmt import administration
import sys,time

try:
	import bach
except:
	bach = "Solid,Unimplimented"

host  = tuple([sys.argv[1],int(sys.argv[2])]) if len(sys.argv)> 2 else ("0.0.0.0", 8090)
	
			

doc = '''This is a XML-RPC based Client Server for general method calls with high efficiency and low hastle.
\n Copyright 2018 BachmanitY Inc.'''

server = SimpleXMLRPCServer(host,allow_none=True)
DocXMLRPCServer.set_server_title(server,server_title='BachmanitY Inc. Servers')
DocXMLRPCServer.set_server_name(server,server_name='Client Server Network BachmanitY Inc.')
DocXMLRPCServer.set_server_documentation(server,server_documentation=doc)

print('Bach-RPC Server Running on host: %s and Port: %s'%host)
print('Server State: %s  Node Status: %s'%tuple(bach.split(',')))
print('Logging is enabled , server started at: %s. \n'%(time.ctime(),))
print('Hit Ctrl + C anytime to hault the server.\n')
server.register_introspection_functions()
server.register_instance( administration() )

try:
	server.serve_forever()
except KeyboardInterrupt:
	print("Server Haulted.")
