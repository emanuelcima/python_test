from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import generics


class Field(models.Model):
    """
    Field Model
    """
    name = models.CharField(max_length=30, primary_key=True)
    hectares = models.DecimalField(max_digits=10, decimal_places=3)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    def __str__(self):
        return self.name


class Rain(models.Model):
    """
    Rain Model
    """
    field = models.ForeignKey(Field, to_field='name', on_delete=models.CASCADE)
    date = models.DateField()
    millimeters = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f'field: {self.field}, date: {self.date}, mm: {self.millimeters}'
