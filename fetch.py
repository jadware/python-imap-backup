import getpass, imaplib, sys, email, os , io
import codecs
from eml import *


def main():

   hostname = 'secure.emailsrvr.com'
   username = 'brianlien2@badvr.com'
   m = imaplib.IMAPClient(hostname, ssl=True)
   m.login(username, 'Feelworld55')

   try:
      print('Start...')

      folderInfoColl = m.list_folders();
      
      print('Done...')

   finally:
      m.logout()

if __name__ == '__main__':
   main()