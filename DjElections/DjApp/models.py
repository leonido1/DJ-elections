from django.contrib.auth.models import User
from django.db import models



class DJ (User):
    pass


class Song (models.Model):
    dj =  models.ManyToManyField(DJ)
    name = models.TextField()
    artist = models.TextField()


class Elections(models.Model):
    dj = models.ForeignKey(DJ, on_delete = models.DO_NOTHING)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

class SongsInElections(models.Model):
    elections = models.ForeignKey(Elections, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    votes =  models.IntegerField()




