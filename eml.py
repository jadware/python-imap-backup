import os
import email
import colorama
from colorama import Fore, Back, Style


def writeEML(path, filename, msg):
	
	os.chdir(path);

	fw = open(path + '/' + filename + '.eml', 'w', encoding="utf-8");
	fw.write(msg);
	fw.close();

	return


def processMailDir(client, mailDir, path):

	dirname = os.path.dirname(__file__);
	
	client.select_folder(mailDir)
	
	messages = client.search(['ALL']);
	
	items = client.fetch(messages, ['UID']).items();
	
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
		subject = envelope.subject.decode();
		
		# extract bytes
		smsg = msg.as_bytes().decode(encoding = 'ISO-8859-1')
		
		# measure size
		size = len(smsg);
		
		# build filename
		filename = str(uid);

		# write the email to disk
		writeEML(dirname + '/' + path, filename, smsg)
		
		
		if size > 1024 * 1024 * 2:
			print(Fore.RED, end='');
		elif size > 1024 * 100:
			print(Fore.YELLOW, end='');
		
		print("\t" + sizefmt(size) + Style.RESET_ALL + "\t{0}\t{1}".format(date_received, ellipsize(subject, 48)));
		return;
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