from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    portfolio = models.JSONField() # storing portfolio as JSON

    def __str__(self):
        return self.username
