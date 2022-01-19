from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=64, null=True, default=None)


class Profile(models.Model):
    user = models.CharField(max_length=64, null=True, default=None)
    description = models.TextField()
    level = models.CharField(max_length=100, null=True, default=None)

class Listing(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=64, null=True, default=None)
    teacher = models.CharField(max_length=64, null=True, default=None)
    subject = models.CharField(max_length=100, null=True, default=None)
    description = models.TextField(null=True, default=None)
    price = models.CharField(max_length=64, null=True, default=None)
    datetime = models.CharField(max_length=1024, null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Student(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class WatchList(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Inquiry(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=1024)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_)










































































































































