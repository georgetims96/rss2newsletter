from django.db import models
from django.shortcuts import render
from rss2newsletters.settings import BASE_DIR
from feedaggregator.models import Entry
from django.template.loader import render_to_string
from newsletter_emailer.email_settings import SENDGRID_API_KEY, FROM_EMAIL
from datetime import datetime
from typing import List
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailHistory:
    def __init__(self, recipients: List[str], entry: Entry):
        self.recipients = recipients
        self.entry = entry
    
    def send_fake(self):
        '''
        (Faked) method to send the included entries to the specified recipients
        '''
        # Use template to render HTML that we will send/save
        html_to_send = render_to_string('newsletter_emailer/email_template.html', {'entry': self.entry})
        self.entry.sent = True
        self.entry.save()
        if self.entry:
            with open(f'{BASE_DIR}/pseudo_emails/{self.entry.feed.title}_most_recent.html', 'w') as f:
                f.write(html_to_send)

    def send(self):
        '''
        Method that leverages SendGrid API to actually send email to relevant recipients 
        '''
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(FROM_EMAIL)
        content = Content("text/html", render_to_string('newsletter_emailer/email_template.html', {'entry': self.entry}))
        # TODO Add relevant daily digest date
        subject = f'{self.entry.title} - {self.entry.feed.title}'
        # Send digest to each recipient
        for recipient in self.recipients:
            to_email = To(recipient.email)
            mail = Mail(from_email, to_email, subject, content)
            res = sg.client.mail.send.post(request_body=mail.get())
        self.entry.sent = True
        self.entry.save()