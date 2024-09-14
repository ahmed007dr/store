from django.db import models

# Create your models here.

class Settings(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to='settings')
    subtitle=models.TextField(max_length=500)
    call_us=models.CharField(max_length=25)
    emails_us=models.TextField(max_length=50)
    emails=models.TextField(max_length=50)
    phone=models.TextField(max_length=50)
    address=models.TextField(max_length=100)

    def __str__(self):
        return self.name
    