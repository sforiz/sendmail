# -*- coding: utf-8 -*-
# Author: dijunzhou@gmail.com

import sys
import os.path
import smtplib
import ConfigParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Send mail config
Host = "smtp.163.com"
Port = "25"
Username = ""
Password = ""

def getcfg(filename):
	"""
		get mail config information.
	"""
	if os.path.isfile(filename):		
		config = ConfigParser.RawConfigParser()
		config.read(filename)
		return config.get("Mail", "To"), config.get("Mail", "Subject"), config.get("Mail", "Body"), config.get("Mail", "MailType"), config.get("Mail", "Attachment"), config.get("Mail", "Cc"), config.get("Mail", "Bcc")

def sendmail(To, Subject, Body, MailType='plain', Attachment='', Cc='', Bcc=''):
  """
  	Send mail by special argument.

  	To: receive addr list
  	Attachment: attachment file path
  """	
  try:
    Subject = Subject.decode('gbk')
    if len(Body) < 80 and os.path.isfile(Body):
      f = open(Body, 'rb')
      Body = f.read().decode('gbk')
      f.close()

    if MailType == 'html':
      msg = MIMEMultipart()
      html = MIMEText(Body, 'html', 'utf8')
      msg.attach(html)

      if Attachment != '' and os.path.isfile(Attachment):
        AttachmentExt = os.path.splitext(Attachment)[-1]
        att = MIMEText(file(Attachment, 'rb').read(), 'base64', 'utf-8')  
        att["Content-Type"] = 'application/octet-stream'  
        att["Content-Disposition"] = 'attachment; filename="attach' + AttachmentExt + '"'  
        msg.attach(att)       
    else:
      msg = MIMEText(Body, 'plain', 'utf-8') 
    msg['To'] = To
    msg['Cc'] = Cc 
    msg['Bcc'] = Bcc 
    msg['Subject'] = Subject
    msg['From'] = Username    
    if Cc != "":
      To += "," + Cc

    smtp = smtplib.SMTP()
    #smtp.set_debuglevel(1)
    smtp.connect(Host, Port)
    smtp.login(Username, Password)
    smtp.sendmail(Username, To.split(','), msg.as_string())
    smtp.quit();
  except Exception, e:
    raise e
  finally:
    pass 

if __name__ == '__main__':  
  To, Subject, Body, MailType, Attachment, Cc = "", "", "", "", "", ""
  #To, Subject, Body, MailType, Attachment, Cc, Bcc = getcfg("mail.cfg")
  # get argument from argv, if argv is valid, ignore main.cfg config information
  argvstart = 1
  MailType = "plain"
  if len(sys.argv) > 1 and (sys.argv[1] == "html" or sys.argv[1] == "plain"):
    MailType = sys.argv[1]
    argvstart = 2  
  if len(sys.argv) == 4 + argvstart - 1:
		To, Subject, Body = sys.argv[argvstart:]
  elif len(sys.argv) == 5 + argvstart - 1:
    To, Cc, Subject, Body = sys.argv[argvstart:]
  if To != "" and Subject != "" and Body != "":
		sendmail(To, Subject, Body, MailType, Attachment, Cc)
  else:
		print "argument is invalid"
