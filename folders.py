import os
import sys
import logging

from imapclient import IMAPClient
from eml import *

if len(sys.argv) != 4:
	print("Usage: python folders.py <server> <username> <password>\n");
	quit();
	
server = sys.argv[1];
username = sys.argv[2];
password = sys.argv[3];

logging.basicConfig(filename=username + ".log", 
					format='%(asctime)s %(message)s', 
					filemode='w');

with IMAPClient(host=server, ssl=True) as client:
	# login
	client.login(username, password)
	
	# get all foldesr
	folders = client.list_folders();

	for flags, delimiter, name in folders:
		os.chdir(os.path.dirname(__file__));
	
		# create folder hierarchy from name, is this correct?
		names = name.split('.');
		
		print(name, end='');
		
		# build path from the hierarchy
		path = "BKUP-" + username + '/' + '/'.join(names);
		
		# create the directory if it doesn't exist
		if not os.path.exists(path):
			os.makedirs(path);

		try:
			select_info = client.select_folder(name);
			num_messages_in_folder = select_info[b'EXISTS'];
			
			print(" (" + str(num_messages_in_folder) + ")");
			
		except:
			print(" (does not exist)");
			logging.warning("could not pull folder \"" + name + "\" because could not select");
			
		