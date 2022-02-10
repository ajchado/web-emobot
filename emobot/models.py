from django.db import models

# Create your models here.
class Person(models.Model):
    personID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=5000)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=20)
    shortbio = models.CharField(max_length=100)
    isLoggedIn = models.BooleanField(default = False)
    isActivated = models.BooleanField(default = False)
    isDeleted = models.IntegerField(default = 0)
    isAdmin = models.BooleanField(default = False)
    profilePicture = models.FileField(default='settings.MEDIA_ROOT/default.jpg')
    image = models.FileField(null=True, blank=True)
    code = models.CharField(max_length=50)

class SessionTable(models.Model):
    SessionID = models.AutoField(primary_key=True)
    personID = models.ForeignKey(Person,on_delete=models.CASCADE)
    Duration = models.IntegerField(default = 0)
    Date = models.CharField(max_length=30)
    Question_Answered = models.CharField(max_length=30)
    
class EmotionTable(models.Model):
    EmotionID = models.AutoField(primary_key=True)
    SessionID = models.ForeignKey(SessionTable,on_delete=models.CASCADE)
    userID = models.ForeignKey(Person,on_delete=models.CASCADE)
    Emotion = models.CharField(max_length=30)
    Time_Recorded = models.CharField(max_length=11)
    

