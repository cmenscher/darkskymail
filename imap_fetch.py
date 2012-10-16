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

  def __init__(self, **settings):
    self.imap_server = settings["imap_server"]
    self.imap_port = settings["imap_port"]
    self.imap_user = settings["imap_user"]
    self.imap_password = settings["imap_password"]
    self.imap_folder = settings.get("imap_folder", None)
    self.use_ssl = settings.get("use_ssl", True)
    self.delete_messages = settings.get("delete_messages", True)
    self.fetch_subject_tag = settings.get("fetch_subject_tag", "[darkskymail]")

  def get_mail(self):
    try:
      if self.use_ssl:
        mbox = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
      else:
        mbox = imaplib.IMAP4(self.imap_server, self.imap_port)
    except:
      typ,val = sys.exc_info()[:2]
      self.error('Could not connect to IMAP server "%s": %s'
          % (self.imap_server, str(val)))

    try:
      typ,dat = mbox.login(self.imap_user, self.imap_password)
    except:
      typ,dat = sys.exc_info()[:2]

    if typ != 'OK':
      self.error('Could not authenticate IMAP connection for "%s" on "%s": %s'
        % (self.imap_user, self.imap_server, str(dat)))

    if self.imap_folder is None:
      self.imap_folder = 'Inbox'

    sel_type,sel_dat = mbox.select(self.imap_folder)
    if(sel_type == "NO"):
      log("IMAP folder '%s' not found.  Creating..." % self.imap_folder)
      mbox.create(self.imap_folder)
      sel_type,sel_dat = mbox.select(self.imap_folder)
      if(sel_type == "NO"):
        error("Could not create IMAP folder %s." % self.imap_folder)

    #typ, dat = mbox.search(None, 'ALL')
    log('Searching for messages whose Subject contains "%s" in folder %s.' % (self.fetch_subject_tag, self.imap_folder))
    typ, dat = mbox.search(None, 'SUBJECT', '"%s"' % self.fetch_subject_tag)

    deleteme = []
    message_content = None

    for num in dat[0].split():
      typ, dat = mbox.fetch(num, '(RFC822)')
      if typ != 'OK':
        self.error(dat[-1])
      message = dat[0][1]

      message_content = self.process_message(message, num)
      deleteme.append(num)

    if len(deleteme) > 0:
      log("%d messages found!" % len(deleteme))

    if self.delete_messages:
      if deleteme == []:
        log('No messages with "%s" in Subject line found in folder %s.' % (self.fetch_subject_tag, self.imap_folder))

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