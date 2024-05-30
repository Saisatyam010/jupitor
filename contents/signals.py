from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Content

@receiver(post_save, sender=Content)
def update_serial_numbers_on_save(sender, instance, **kwargs):
    if not instance.pk:
        # If it's a new instance, update serial numbers for all contents of the same title and product
        contents = Content.objects.filter(title=instance.title, product=instance.product).order_by('serial_number')
        for index, content in enumerate(contents):
            content.serial_number = index + 1
            content.save()

@receiver(post_delete, sender=Content)
def update_serial_numbers_on_delete(sender, instance, **kwargs):
    # Update serial numbers of remaining contents after the deleted content
    contents = Content.objects.filter(title=instance.title, product=instance.product, serial_number__gt=instance.serial_number).order_by('serial_number')
    for content in contents:
        content.serial_number -= 1
        content.save()
