# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


class FirmProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=300, null=True)
    company_email = models.EmailField(null=True)
    company_telephone = models.CharField(max_length=100, null=True)
    company_address1 = models.CharField(max_length=1000, null=True)
    company_address2 = models.CharField(max_length=1000, null=True)
    company_country = models.CharField(max_length=100, null=True)
    company_state = models.CharField(max_length=100, null=True)
    company_city = models.CharField(max_length=100, null=True)
    company_zip = models.CharField(max_length=100, null=True)
    company_gstn = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firm_id = models.ForeignKey(FirmProfile, on_delete=models.CASCADE, null=True)
    TYPE = (
        ('Driver', 'Driver'),
        ('Owner', 'Owner'),
        ('SysAdmin', 'SysAdmin')
    )
    usertype = models.CharField(max_length=100, null=True, choices=TYPE)
    email_is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class StationReport(models.Model):
    vin = models.CharField(max_length=100)
    s1_start = models.DateTimeField(null=True, blank=True)
    s1_end = models.DateTimeField(null=True, blank=True)
    s1_error = models.CharField(max_length=100, null=True, blank=True)
    s2_start = models.DateTimeField(null=True, blank=True)
    s2_end = models.DateTimeField(null=True, blank=True)
    s2_error = models.CharField(max_length=100, null=True, blank=True)
    s3_start = models.DateTimeField(null=True, blank=True)
    s3_end = models.DateTimeField(null=True, blank=True)
    s3_error = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.vin


class TagAssign(models.Model):
    vin = models.CharField(max_length=100, blank=True, null=True)
    tag_id = models.CharField(max_length=50)
    station_pos = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.tag_id
