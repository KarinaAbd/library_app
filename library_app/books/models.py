from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    url = models.URLField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
