from django.db import models

# Create your models here.
class Email:
    def __init__(self, recipients, entry):
        self.recipients = recipients
        self.entry = entry
    
    def send(self):
        self.entry.sent = True
        self.entry.save()
