import os
import sys

from imapclient import IMAPClient
from eml import *


if len(sys.argv) != 4:
	print("Usage: python folders.py <server> <username> <password>\n");
	quit();
	
server = sys.argv[1];
username = sys.argv[2];
password = sys.argv[3];

with IMAPClient(host=server, ssl=True) as client:
	# login
	client.login(username, password)
	
	# get all foldesr
	folders = client.list_folders();

	for flags, delimiter, name in folders:
		os.chdir(os.path.dirname(__file__));
	
		# create folder hierarchy from name, is this correct?
		names = name.split('.');
		
		# build path from the hierarchy
		path = "BKUP-" + username + '/' + '/'.join(names);
		
		# create the directory if it doesn't exist
		if not os.path.exists(path):
			os.makedirs(path);

		select_info = client.select_folder(name);
		num_messages_in_folder = select_info[b'EXISTS'];

		print(name + " (" + str(num_messages_in_folder) + ")");

		processMailDir(client, name, path);