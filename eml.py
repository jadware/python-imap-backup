import time
import datetime
from datetime import timezone
import filedate
import os
import email
import colorama
from colorama import Fore, Back, Style


def writeEML(path, filename, msg, date_received):
	full_path = path + '/' + filename + '.eml';
	
	# write the message to disk with UTF-8 encoding - should this be unicode?
	with open(full_path, 'w', encoding="utf-8") as fw:
		fw.write(msg);
		fw.flush();
	
	file = filedate.File(full_path);
	file.set(
		created = date_received,
		modified = date_received,
		accessed = date_received
	);
	
	return;


def processMailDir(client, mailDir, path):

	dirname = os.path.dirname(__file__);
	
	client.select_folder(mailDir)
	
	messages = client.search(['ALL']);
	
	chunk = 100;
	
	for i in range(0, len(messages), chunk):
		
		items = client.fetch(messages[i:i + chunk], ['UID']).items();
		
		for uid, message_data in items:
			print("#" + str(uid), end='');
			
			# pull message and envelope
			item = client.fetch([uid], ['ENVELOPE', 'RFC822'])[uid];
			
			# extract envelope
			envelope = item[b'ENVELOPE'];
			
			# pull date the message was received
			date_received = envelope.date;
			
			# extract message content
			msg = email.message_from_bytes(item[b'RFC822']);
			
			# decode subject into a string, though it probably should be unicode not utf
			if envelope.subject is None:
				subject = "(None)";
			else:
				subject = envelope.subject.decode();
			
			# extract bytes
			smsg = msg.as_bytes().decode(encoding = 'ISO-8859-1')
			
			# measure size
			size = len(smsg);
			
			if date_received is None:
				date_utc = "(None)";
			else:
				date_utc = date_received.replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H%M%S");
			
			# build filename
			filename = date_utc + ' - ' + str(uid);

			# write the email to disk
			writeEML(dirname + '/' + path, filename, smsg, date_received)
			
			if size > 1024 * 1024 * 2:
				print(Fore.RED, end='');
			elif size > 1024 * 100:
				print(Fore.YELLOW, end='');
			
			print("\t" + sizefmt(size) + Style.RESET_ALL + "\t{0}\t{1}".format(date_received, ellipsize(subject, 48)));

	return;


def sizefmt(num):
	suffix = "B"

	for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
		if abs(num) < 1024.0:
			return f"{num:3.1f}{unit}{suffix}"

		num /= 1024.0
		
	return f"{num:.1f}Y{suffix}"


def ellipsize(str_input, max_length):
    str_end = '...'
	
    length = len(str_input)
	
    if length > max_length:
        return str_input[:max_length - len(str_end)] + str_end

    return str_input