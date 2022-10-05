from django.db import models
from django.shortcuts import render
from rss2newsletters.settings import BASE_DIR
from django.template.loader import render_to_string


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
  