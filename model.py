# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ReportsReport(models.Model):
    trip_id = models.IntegerField(db_column='TRIP_ID')  # Field name made lowercase.
    startedt = models.DateTimeField(db_column='STARTEDT')  # Field name made lowercase.
    endedt = models.DateTimeField(db_column='ENDEDT', blank=True, null=True)  # Field name made lowercase.
    startlat = models.CharField(db_column='STARTLAT', max_length=100)  # Field name made lowercase.
    endlat = models.CharField(db_column='ENDLAT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    startlng = models.CharField(db_column='STARTLNG', max_length=100)  # Field name made lowercase.
    endlng = models.CharField(db_column='ENDLNG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    startodo = models.FloatField(db_column='STARTODO')  # Field name made lowercase.
    endodo = models.FloatField(db_column='ENDODO', blank=True, null=True)  # Field name made lowercase.
    startaddress = models.CharField(db_column='STARTADDRESS', max_length=500)  # Field name made lowercase.
    endaddress = models.CharField(db_column='ENDADDRESS', max_length=500, blank=True, null=True)  # Field name made lowercase.
    max_speed = models.FloatField(db_column='MAX_SPEED', blank=True, null=True)  # Field name made lowercase.
    avg_speed = models.FloatField(db_column='AVG_SPEED', blank=True, null=True)  # Field name made lowercase.
    device = models.ForeignKey('UserformsDevice', models.DO_NOTHING)
    driver = models.ForeignKey('UserformsDriver', models.DO_NOTHING)
    firm = models.ForeignKey('AppFirmprofile', models.DO_NOTHING)
    vehicle = models.ForeignKey('UserformsVehicle', models.DO_NOTHING)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_report'
