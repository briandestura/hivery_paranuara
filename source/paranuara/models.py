from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'company'


class People(models.Model):
    index = models.AutoField(primary_key=True, db_column='id')
    _id = models.CharField(max_length=255, blank=True, null=True)
    guid = models.CharField(max_length=255, blank=True, null=True)
    has_died = models.BooleanField(default=False)
    balance = models.CharField(max_length=255, blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    age = models.PositiveIntegerField(default=0)
    eyeColor = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    registered = models.DateTimeField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    greeting = models.TextField(blank=True, null=True)
    favorite_fruits = models.TextField(blank=True, null=True)
    favorite_vegetables = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'people'


class Friendship(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    friend = models.ForeignKey(People, related_name='friend', on_delete=models.CASCADE)

    class Meta:
        db_table = 'friendship'
        unique_together = ('person', 'friend')