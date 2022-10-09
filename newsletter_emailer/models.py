from django.db import models
from django.shortcuts import render
from rss2newsletters.settings import BASE_DIR
from django.template.loader import render_to_string
from newsletter_emailer.email_settings import SENDGRID_API_KEY, FROM_EMAIL
from datetime import datetime
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

class Email:
    def __init__(self, recipients, entries):
        self.recipients = recipients
        self.entries = entries
    
    def send(self):
        '''
        Method we will ulitmately use to send the included entries to the specified recipients
        '''
        # Use template to render HTML that we will send/save
        html_to_send = render_to_string('newsletter_emailer/email_template.html', {'entries': self.entries})
        for entry in self.entries:
            entry.sent = True
            entry.save()
        if self.entries:
            with open(f'{BASE_DIR}/pseudo_emails/{self.entries[0].feed.title}_most_recent.html', 'w') as f:
                f.write(html_to_send)
    
    def send_real(self):
        '''
        Method that will actually send email to relevant recipients 
        '''
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(FROM_EMAIL)
        content = Content("text/email", render_to_string('newsletter_emailer/email_template.html', {'entries': self.entries}))
        # TODO Add relevant daily digest date
        subject = f'{self.entries.first().feed.title} Daily Digest'
        # Send digest to each recipient
        for recipient in self.recipients:
            to_email = To(recipient.email)
            mail = Mail(from_email, to_email, subject, content)
            res = sg.client.mail.send.post(request_body=mail.get())