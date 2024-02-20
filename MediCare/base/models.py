from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic =  models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Massage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    
class Patient(models.Model):
    Patient_ID = models.AutoField(primary_key = True)
    Patient_Name = models.CharField(max_length=200)
    Patient_Email = models.CharField(max_length=255)
    Patient_Password = models.CharField(max_length=255)
    Patient_Address = models.CharField(max_length=255)
    Patient_Family_Medical_History = models.ImageField(upload_to='static/Image')

    def __str__(self):
        return self.Patient_Name

class Admin(models.Model):
    Admin_ID = models.AutoField(primary_key = True)
    Admin_Name = models.CharField(max_length=200)
    Admin_Email = models.CharField(max_length=255)
    Admin_Password = models.CharField(max_length=200)

    def __str__(self):
        return self.Admin_Name

class Doctor(models.Model):
    Doctor_ID = models.AutoField(primary_key = True)
    Doctor_Name = models.CharField(max_length=200)
    Doctor_Email = models.CharField(max_length=255)
    Doctor_Password = models.CharField(max_length=200)
    Doctor_Address = models.CharField(max_length=255)
    Doctor_License = models.ImageField(upload_to='static/Image')
    Admin_ID = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.Doctor_Name

class Feedback(models.Model):
    Feedback_ID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=200)
    Message = models.TextField()
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title
    




