from django.db import models
from userforms.models import *
from app.models import *


class Report(models.Model):
    TRIP_ID = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    firm = models.ForeignKey(FirmProfile, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    STARTEDT = models.DateTimeField()
    ENDEDT = models.DateTimeField(null=True)
    STARTLAT = models.CharField(max_length=100)
    ENDLAT = models.CharField(max_length=100, null=True)
    STARTLNG = models.CharField(max_length=100)
    ENDLNG = models.CharField(max_length=100, null=True)
    STARTODO = models.FloatField()
    ENDODO = models.FloatField(null=True)
    STARTADDRESS = models.CharField(max_length=500)
    ENDADDRESS = models.CharField(max_length=500, null=True)
    MAX_SPEED = models.FloatField(null=True)
    AVG_SPEED = models.FloatField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} {1}'.format(self.TRIP_ID, self.firm)
