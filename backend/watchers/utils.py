# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 2021
@author: sagrana
"""
import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "my@gmail.com"  # Enter your address
receiver_email = "your@gmail.com"  # Enter receiver address
password = "testt"


def notify_user(watcher_id):
    # Fetch information for Email Body using watcher id
    print("Email Sent!!")
    message = "Watcher Added"
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)
