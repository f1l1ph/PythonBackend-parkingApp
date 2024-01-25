from django.db import models

# Create your models here.
class GeeksModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
 
    def __str__(self):
        return self.title
    

class Car(models.Model):
    licensePlate = models.CharField(max_length=7)
    brandName = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

class Person(models.Model):
    name = models.CharField(max_length=30)
    car = Car

