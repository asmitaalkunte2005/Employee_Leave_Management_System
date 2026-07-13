from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee_profile')
    employee_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.name

