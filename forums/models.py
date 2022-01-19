from django.db import models
#from django.contrib.auth.models import AbstractUser
# Create your models here.

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1024, default=None, null=True)
    category = models.CharField(max_length=1024, default=None, null=True)
    content = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=1024)

class Liker(models.Model):
    post_id = models.IntegerField()
    user = models.CharField(max_length=1024)

class Comment(models.Model):
    post_id = models.IntegerField()
    content = models.CharField(max_length=1024)
    indivcomment_id = models.IntegerField()
    user = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)

class LikeComment(models.Model):
    comment_id = models.IntegerField()
    user = models.CharField(max_length=1024)

class Tag(models.Model):
    post_id = models.IntegerField()
    name = models.CharField(max_length=1024)