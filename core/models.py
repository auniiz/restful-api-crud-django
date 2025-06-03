from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey('Employee', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_departments')

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    manager = models.BooleanField(default=False)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
