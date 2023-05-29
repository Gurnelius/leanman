from django.db import models


class Tweet(models.Model):
    created_at = models.DateTimeField()
    id = models.BigIntegerField(primary_key=True)
    full_text = models.TextField()
    retweet_count = models.IntegerField()
    favorite_count = models.IntegerField()
    
    def __str__(self):
        return self.full_text