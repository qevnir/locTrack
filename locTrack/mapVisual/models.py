from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# Create your models here.

class TrackPointManager(models.Manager):

    def create_trackpoint(self, point):
        try:
            point = self.create(timestamp=point.time,
                                point=Point(point.longitude, point.latitude),
                                elevation=point.elevation,
                                speed=point.speed)
        except Exception:
            error_msg= ("Invalid data in trackpoint!")
            print(error_msg)
        
    

class TrackPoint(models.Model):
    timestamp = models.DateTimeField()
    point = models.PointField(geography=True)
    elevation = models.FloatField()
    speed = models.FloatField(null=True)

    objects = TrackPointManager()

class Location(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    time_until_visited = models.IntegerField()
    color = models.CharField(max_length=7)
    polygon = models.PolygonField()
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
