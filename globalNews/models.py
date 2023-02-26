from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    profile_pic = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return f"Username: {self.username}, email: {self.email}"


class Topic(models.Model):
    pass
    topic = models.TextField(default="", max_length=25)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed_topics")

    def __str__(self):
        return f"{self.follower.username} is intersted in {self.topic} news articles"


class SavedArticle(models.Model):
    saver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_saved_articles")
    title = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=250, default="")
    articleUrl = models.URLField(null=True, blank=True, default="")
    thumbnailUrl = models.URLField(null=True, blank=True, default="")
    publishDate = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=20, default="")

    def __str__(self):
        return f"{self.title} ,By {self.source}"
