from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pin = models.IntegerField(null=True, default=None)
    first_name = models.CharField(max_length=64, null=True, default=None)


class Profile(models.Model):
    user = models.CharField(max_length=64, null=True, default=None)
    description = models.TextField()
    qualifications = models.TextField(null=True)
    level = models.CharField(max_length=100, null=True, default=None)
    url = models.CharField(max_length=200, null=True)
    file = models.FileField(upload_to='media', default=None, null=True)


class Notifications(models.Model):
    user = models.CharField(max_length=64, null=True, default=None)
    info = models.CharField(max_length=1024, null=True, default=None)
    category = models.CharField(max_length=64, null=True, default=None)
    notifid = models.IntegerField(null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    read = models.BooleanField(default=None)


class Listing(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=64, null=True, default=None)
    teacher = models.CharField(max_length=64, null=True, default=None)
    subject = models.CharField(max_length=100, null=True, default=None)
    description = models.TextField(null=True, default=None)
    price = models.CharField(max_length=64, null=True, default=None)
    datetime = models.CharField(max_length=1024, null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    announcement = models.TextField(null=True, default=None)

class Student(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class WatchList(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Inquiry(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=1024, null=True, default=None)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Timeslots(models.Model):
    listingid = models.IntegerField()
    #customer = models.CharField(max_length=64, null=True, default=None)
    timeslotid = models.IntegerField(default=None, null=True)
    timeslot = models.CharField(max_length=1024, null=True, default=None)
    selected = models.BooleanField(default=None)
    limitpax = models.IntegerField(default=None, null=True)

class Customers(models.Model):
    #to reference timeslotid
    customerid = models.IntegerField(default=None, null=True)
    customer = models.CharField(max_length=64)


class Rating(models.Model):
    teacher_user = models.CharField(max_length=64)
    subject = models.CharField(max_length=100, null=True)
    score = models.IntegerField()
    feedback = models.TextField(null=True)

#class Announcement(models.Model):
    #user = models.CharField(max_length=64)
    #content = models.TextField()
    #listingid = models.IntegerField()
    #timestamp = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    #chat_id = models.IntegerField()
    user = models.CharField(max_length=64, null=True)
    contact = models.CharField(max_length=64, null=True)

class Messages(models.Model):
    #message_id=models.IntegerField(default=None, null=True)
    read = models.BooleanField(default=None)
    sender = models.CharField(max_length=64)
    receiver = models.CharField(max_length=64)
    content = models.TextField(null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "message_id": self.message_id,
            "read": self.read,
            "sender": self.sender,
            "receiver": self.receiver,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content
           }

class Mode(models.Model):
    mode = models.CharField(default="student", max_length=64)
    user = models.CharField(max_length=64, null=True)





