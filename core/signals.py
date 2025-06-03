import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Employee

@receiver(post_delete, sender=Employee)
def delete_employee_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
        except Exception as e:
            print(f"Error deleting file: {e}")
