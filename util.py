import smtplib
import os, sys
import shutil
import re

import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from email.Iterators import body_line_iterator, typed_subpart_iterator
import imaplib

import httplib, urllib, urllib2, sys
import json

import settings

class IMAP_Fetch:

  def get_mail(self, host, imap_user, imap_password, delete_messages=False):
    try:
      #mbox = imaplib.IMAP4(host)
      mbox = imaplib.IMAP4_SSL(host, 993)
    except:
      typ,val = sys.exc_info()[:2]
      self.error('Could not connect to IMAP server "%s": %s'
          % (host, str(val)))

    try:
      typ,dat = mbox.login(imap_user, imap_password)
    except:
      typ,dat = sys.exc_info()[:2]

    if typ != 'OK':
      self.error('Could not open INBOX for "%s" on "%s": %s'
        % (imap_user, host, str(dat)))

    mbox.select('Inbox')
    typ, dat = mbox.search(None, 'ALL')
    mbox.create("DarkSkyMail")

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
        log("Moving message to 'Processed' folder...")
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


def send_mail(smtp_server, smtp_user, smtppass, port, to, fro, subject, text, html="", attachment=None):
  """
    USAGE: send_mail("smtp.gmail.com", alertFrom, alertPass, 587, [alertTo], alertFrom, subj, body,["/path/to/file/include"])
  """
  assert type(to)==list

  if html != "":
    msg = MIMEMultipart('alternative')
  else:
    msg = MIMEMultipart()

  msg['From'] = fro
  msg['To'] = COMMASPACE.join(to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )
  #part.set_payload( open(filename,"rb").read() )
  #Encoders.encode_base64(part)
  #part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filetitle))
  if attachment:
    attachment_part = MIMEBase('application', "octet-stream")
    try:
        filename = str(attachment["filename"]).strip()
        filetitle = str(attachment["title"]).strip()
        if filetitle == "":
          filetitle = os.path.basename(filename)
        filetitle = filetitle + "." + str(attachment["type"]).lower()
        attachment_part.set_payload( open(filename,"rb").read() )
        Encoders.encode_base64(part)
        attachment_part.add_header('Content-Disposition', 'attachment; filename="%s"' % filetitle)
        msg.attach(attachment_part)
    except:
        attachment_part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        attachment_part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(attachment_part)

  part1 = MIMEText(text, 'plain')
  msg.attach(part1)

  if html != "":
    part2 = MIMEText(html, 'html')
    msg.attach(part2)

  smtp = smtplib.SMTP(smtp_server, port)
  smtp.ehlo()
  smtp.starttls()
  smtp.ehlo
  smtp.login(smtp_user, smtppass)
  smtp.sendmail(fro, to, msg.as_string() )
  smtp.close()
  return 1


def search_for_venue(query):
  """
    This will call the Google Geocoding API to look for a venue that matches the location
  """

  query = query.replace(" ", "+")
  base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
  params = "address=%s&sensor=false" % query
  google_url = "%s%s" % (base_url, params)
  geo_data = None

  req = None
  try:
    req = urllib2.urlopen(google_url)
    geo_data = req.read()
  except urllib2.HTTPError, e:
    log("ERROR: %s: %s" % (e.code, e.read()))
    exit (1)

  return geo_data


def get_forecast(api, lat, lon):
  """
    This will use the Dark Sky REST API to get the forecast at the passed coords
  """

  forecast_data = None
  forecast_url = "https://api.darkskyapp.com/v1/brief_forecast/%s/%d,%d" % (api, lat, lon)

  req = None
  try:
    req = urllib2.urlopen(forecast_url)
    forecast_data = req.read()
  except urllib2.HTTPError, e:
    log("ERROR: %s: %s" % (e.code, e.read()))
    exit (1)

  return forecast_data

def log(msg, skip=False):
    dsm_settings = settings.Dark_Sky_Mail_Settings()
    if dsm_settings.show_log:
      sys.stderr.write('%s\n' % msg)
