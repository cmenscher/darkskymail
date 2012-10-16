import os, sys
from util import log
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from email.Iterators import body_line_iterator, typed_subpart_iterator
import imaplib

class IMAP_Fetch:

  def get_mail(self, host, port, imap_user, imap_password, use_ssl=True, delete_messages=False, imap_folder=None):
    try:
      if use_ssl:
        mbox = imaplib.IMAP4_SSL(host, port)
      else:
        mbox = imaplib.IMAP4(host, port)
    except:
      typ,val = sys.exc_info()[:2]
      self.error('Could not connect to IMAP server "%s": %s'
          % (host, str(val)))

    try:
      typ,dat = mbox.login(imap_user, imap_password)
    except:
      typ,dat = sys.exc_info()[:2]

    if typ != 'OK':
      self.error('Could not authenticate IMAP connection for "%s" on "%s": %s'
        % (imap_user, host, str(dat)))

    if imap_folder:
      sel_type,sel_dat = mbox.select(imap_folder)
      if(sel_type == "NO"):
        log("IMAP folder '%s' not found.  Creating..." % imap_folder)
        mbox.create(imap_folder)
        sel_type,sel_dat = mbox.select(imap_folder)
        if(sel_type == "NO"):
          error("Could not create IMAP folder %s." % imap_folder)
    else:
      mbox.select() #defaults to 'INBOX'

    typ, dat = mbox.search(None, 'ALL')

    deleteme = []
    message_content = None
    for num in dat[0].split():
      typ, dat = mbox.fetch(num, '(RFC822)')
      if typ != 'OK':
        self.error(dat[-1])
      message = dat[0][1]

      #not sure if dat[0][0] is actually the subject!
      headers = str(dat[0][1])
      index = -1
      index = headers.index("darkskymail")

      if(index > 0):
        message_content = self.process_message(message, num)
        deleteme.append(num)
      else:
        log("Message %s does not have [darkskymail] in subject line." % num)

    if delete_messages:
      if deleteme == []:
        log("No mails to be processed were found.")

      deleteme.sort()
      for number in deleteme:
        log("Deleting event data message...")
        mbox.copy(number, 'Processed')
        mbox.store(number, "+FLAGS.SILENT", '(\\Deleted)')

    mbox.expunge()
    mbox.close()
    mbox.logout()

    return message_content


  def error(self, reason):
    sys.stderr.write('%s\n' % reason)
    sys.exit(1)

  def process_message(self, email_text, msgnum):
    """ 
      Loop over each line of the message to get the content
    """
    msg = email.message_from_string(email_text)
    bodylines = list(typed_subpart_iterator(msg, "text", "plain"))
    message_content = None
    while(bodylines):
      line = bodylines.pop(0)
      thisline = str(line).strip()
      thisline_escaped = thisline.encode('string-escape')
      headerEnd = thisline.find("\n\n") #end of the mail headers
      headerEnd = headerEnd + 2 #ignore the \n's
      msg_txt = thisline[headerEnd:]
      message_content = str(msg_txt)

    return message_content
