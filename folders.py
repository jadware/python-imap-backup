import os
import sys

from imapclient import IMAPClient
from eml import *


if len(sys.argv) != 4:
	print("Usage: python folders.py <server> <username> <password>\n");
	quit();

with IMAPClient(host=sys.argv[1], ssl=True) as client:
	client.login(sys.argv[2], sys.argv[3])

	folders = client.list_folders();

	for flags, delimiter, name in folders:
		names = name.split('.');
		path = os.path.join(*names);
		
		print(path);

		if not os.path.exists(path):
			os.mkdir(path);

		select_info = client.select_folder(name);
		num_messages_in_folder = select_info[b'EXISTS'];

		print(name + " (" + str(num_messages_in_folder) + ")");

		processMailDir(client, name, path);