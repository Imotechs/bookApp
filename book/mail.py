from django.core.mail import EmailMessage  
from django.shortcuts import render,redirect

from django.template.loader import render_to_string  
from email import message as MSG
from django.contrib.auth.models import User
import smtplib
import datetime
from django.conf import settings
username = settings.EMAIL_HOST_USER
password= settings.EMAIL_HOST_PASSWORD


def send_admin_mail(check_in_book):
        msg = MSG.EmailMessage()
        #get all librarians
        admins = User.objects.filter(is_superuser = True)
        #send all librarians mails of the book instance
        for user in admins:
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('admi_report_email.html', {  
                'user': user,
                'book':check_in_book,
            })  
            to_email = user.email 
            
            msg['To'] =  to_email
            msg['subject'] = 'Book Not checked in'
            msg['From'] =f'noreply<{username}>'
            msg.set_content(message,subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(username, password)
                try:
                    smtp.send_message(msg)
                except Exception as error:
                    pass
                return True 