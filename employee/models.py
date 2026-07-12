from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.name

