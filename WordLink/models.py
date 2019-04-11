from django.db import models

# Create your models here.
# Create your models here.
class word_link(models.Model):
    username = models.CharField(max_length=100)
    word_searched = models.CharField(max_length=100)
    result = models.CharField(max_length=100000)
    date_time = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.word_searched
