#!/usr/bin/env python

import smtplib
import os
import ConfigParser
import backup
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmail(subject=None,strmsg=None):
    '''Sends an email'''
    
    # me == my email address
    # you == recipient's email address
	#Credentials
    username = 'sunnyhillsveterinaryhospital@gmail.com'
    password = ''	
    me = 'messenger@sunnyhillsveterinaryhospital.com'
    emailto = ['eromero506@gmail.com', 'johann.romero@gmail.com']
    strmailgw = 'smtp.gmail.com'
    newmsg = email.message_from_string(strmsg)
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ', '.join(emailto) 


    # Create the body of the message (a plain-text and an HTML version).
    if newmsg.is_multipart():
        for payload in newmsg.get_payload():
            # if payload.is_multipart(): ...
            #print payload.get_payload()
            text = payload.get_payload()
    else:
        #print newmsg.get_payload()
        text = newmsg.get_payload()
    #text = strmsg
    html = """<html><head></head><body><p>Hi!<br></p></body></html>"""

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    #msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(strmailgw)
    #Enable secure connection to gmail smtp
    s.starttls()
    #Set credentials to send email via gmail
    s.login(username,password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, emailto, msg.as_string())
    s.quit()
