from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee, Department, Position, Status

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Status)
