from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    finishNum = models.IntegerField()
class Email(models.Model):
    email = models.EmailField()
    validate = models.CharField(max_length=8)
    def __str__(self):
        return self.email