from django.db import models
from rest_framework import generics


class Field(models.Model):
    """Field Model"""
    name = models.CharField(max_length=30, primary_key=True)
    hectares = models.DecimalField(max_digits=10, decimal_places=3)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.name


class Rain(models.Model):
    """Rain Model"""
    date = models.DateField()
    millimeters = models.DecimalField(max_digits=10, decimal_places=3)
    field = models.ForeignKey(Field, to_field='name', on_delete=models.CASCADE)

    def __str__(self):
        return f'field: {self.field}, date: {self.date}, mm: {self.millimeters}'
