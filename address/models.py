from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=200)
    tel = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.name