from django.db import models
# Create your models here.


class Weather(models.Model):
    date = models.DateField()
    lat = models.DecimalField(max_digits=7, decimal_places=4)
    lon = models.DecimalField(max_digits=7, decimal_places=4)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)


class Temperature(models.Model):
    temperature = models.DecimalField(max_digits=7, decimal_places=1)
    weather = models.ForeignKey(Weather, related_name='temperatures', on_delete=models.CASCADE)

