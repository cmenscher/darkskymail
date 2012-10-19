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
    self.event_notification_search_criteria = settings.get("fetch_from_address", "calendar-notification@google.com")

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

    log('Searching for messages from "%s" in folder %s.' % (self.event_notification_search_criteria, self.imap_folder))
    typ, dat = mbox.search(None, 'FROM', '"%s"' % self.event_notification_search_criteria)

    deleteme = []
    message_content = None

    for num in dat[0].split():
      typ, dat = mbox.fetch(num, '(RFC822)')
      if typ != 'OK':
        self.error(dat[-1])
      message = dat[0][1]

      message_content = self.process_message(message)
      deleteme.append(num)

    if len(deleteme) > 0:
      log("%d messages found!" % len(deleteme))

    if self.delete_messages:
      if deleteme == []:
        log('No messages with "%s" in From address found in folder %s.' % (self.event_notification_search_criteria, self.imap_folder))

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


  def process_message(self, email_text, decode=True):
    """ 
      Loop over each part of the message to get the content.
    """
    msg = email.message_from_string(email_text)
    message_content = list()

    msg_payload_type = None
    msg_payload_body = None
    parts = list(typed_subpart_iterator(msg, "text"))
    for part in parts:
        msg_payload_type = part.get_content_type()
        msg_payload_body = part.get_payload(None, True) #True decodes base64 if necessary
        message_content.append({msg_payload_type: msg_payload_body})
    #log(message_content)
    return message_content

