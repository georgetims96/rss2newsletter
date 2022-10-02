from django.db import models
from rss2newsletters.settings import BASE_DIR


# Create your models here.
class Email:
    def __init__(self, recipients, entries):
        self.recipients = recipients
        self.entries = entries
    
    def send(self):
        html_to_send = self.__gen_email_html()
        for entry in self.entries:
            entry.sent = True
            entry.save()
        if self.entries:
            with open(f'{BASE_DIR}/pseudo_emails/{self.entries[0].feed.title}_most_recent.html', 'w') as f:
                f.write(html_to_send)
    
    def __gen_email_html(self):
        '''
        Private method that converts list of Entry objects
        into an email body we'll send to subscribers
        '''
        html_to_return = ""
        for entry in self.entries:
            title_html = f'<h1>{entry.title}</h1>'
            body_html = entry.body
            html_to_return = html_to_return + title_html + body_html + "<hr />"
        return html_to_return

