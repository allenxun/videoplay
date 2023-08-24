from django.db import models

# Create your models here.


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    videoId = models.ForeignKey('VideoInfo', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    episode = models.CharField(max_length=20)
    path = models.CharField(max_length=100)

    
class VideoInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    episode = models.CharField(max_length=20)