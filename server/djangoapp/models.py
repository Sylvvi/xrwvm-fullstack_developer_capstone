from django.db import models


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

    make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name='models'
    )
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPE_CHOICES,
        default='SEDAN'
    )
    year = models.DateField()

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year.year})"
