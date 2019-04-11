from django.db import models

# Create your models here.
# Create your models here.
class user(models.Model):

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100000)
    email = models.CharField(max_length=30)
    date_time = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return (self.username+" ")
