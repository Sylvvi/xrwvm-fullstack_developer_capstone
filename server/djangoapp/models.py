from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation


class CarModel(models.Model):
    CAR_TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        # Add more choices as required
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')  # Many-to-One relationship
    dealer_id = models.IntegerField()  # Refers to a dealer created in Cloudant database
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES, default='SEDAN')
    year = models.DateField()  # Updated to DateField for the year

    # Other fields as needed

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year.year})"  # Print car make and model

