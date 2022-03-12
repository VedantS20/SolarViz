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



class SolarDBConfig(models.Model):
    id = models.IntegerField(default=1,null=False,primary_key=True)
    selectedTables = models.CharField(max_length=1100,blank=True,null=True)
    host = models.CharField(max_length=50,blank=True,null=True)
    user = models.CharField(max_length=50,blank=True,null=True)
    database = models.CharField(max_length=50,blank=True,null=True)
    password = models.CharField(max_length=50,blank=True,null=True)


    def __str__(self):
        return self.host