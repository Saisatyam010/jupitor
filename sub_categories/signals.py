# sub_categories/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SubCategory

@receiver(post_save, sender=SubCategory)
def subcategory_saved(sender, instance, created, **kwargs):
    if created:
        print(f"SubCategory {instance.name} created.")
    else:
        print(f"SubCategory {instance.name} updated.")

@receiver(post_delete, sender=SubCategory)
def subcategory_deleted(sender, instance, **kwargs):
    print(f"SubCategory {instance.name} deleted.")
