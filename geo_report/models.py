from django.db import models


class GeoReport(models.Model):
    id = models.UUIDField(primary_key=True)
    long = models.FloatField()
    lat = models.FloatField()
    timestamp = models.BigIntegerField()
    accuracy = models.FloatField()
    deviceId = models.TextField(max_length=30)


    def __str__(self):
        return str(self.id) + ' - ' + "long: " + str(self.long) + " lat: " + str(self.lat) + ' ' + str(self.timestamp)