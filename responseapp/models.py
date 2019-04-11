from django.db import models

# Create your models here.
class feedback(models.Model):

    name = models.CharField(max_length=100)
    link=models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    feedback=models.CharField(max_length=3000)
    date_time = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return (self.username+" ")
