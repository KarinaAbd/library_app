from django.db import models
from datetime import datetime

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
