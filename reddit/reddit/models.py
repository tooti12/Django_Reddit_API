from django.db import models
from datetime import datetime

class Post(models.Model):
    """Model to store posts
    """

    post_id = models.CharField(max_length=15,unique=True)
    title = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return self.post_id
