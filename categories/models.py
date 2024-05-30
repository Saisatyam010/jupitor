# categories/models.py
from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    serial_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    subcategory_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.serial_number:
            last_category = Category.objects.order_by('serial_number').last()
            if last_category:
                self.serial_number = last_category.serial_number + 1
            else:
                self.serial_number = 1
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
