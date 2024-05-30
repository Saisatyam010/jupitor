# categories/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Category

@receiver(post_delete, sender=Category)
def reassign_serial_numbers(sender, instance, **kwargs):
    categories = Category.objects.all().order_by('serial_number')
    for index, category in enumerate(categories, start=1):
        if category.serial_number != index:
            category.serial_number = index
            category.save()
